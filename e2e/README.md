# E2E Tests

End-to-end tests run against a real Home Assistant instance with Mosquitto MQTT broker,
both running in Docker. The integration is mounted as a volume into the HA container.

## Prerequisites

- Docker and Docker Compose
- Python 3.12+

## Quick start

```bash
cd e2e
./run.sh
```

The script will:
1. Stop any previous containers and volumes
2. Start Home Assistant + Mosquitto via Docker Compose
3. Create a Python venv with test dependencies (first run only)
4. Wait for HA to be ready (up to 3 minutes)
5. Run all E2E tests
6. Tear down containers on exit

## Manual run

```bash
# Start services
docker compose -f e2e/docker-compose.yml up -d

# Wait for HA (check http://localhost:8123/api/onboarding)

# Run tests
cd e2e
python -m pytest test_e2e.py -v --tb=short
```

## Architecture

```
Host machine                    Docker network
+------------------+           +------------------+
| test_e2e.py      |           | homeassistant    |
|   - onboards HA  |  :8123    |   - loads        |
|   - REST API     | --------> |     whatwatt from |
|   - publishes    |           |     /config/      |
|     MQTT         |  :1883    |     custom_comp.  |
|                  | --------> +------------------+
+------------------+           | mosquitto        |
                               |   - MQTT broker  |
                               +------------------+
```

The test runner:
- Performs HA onboarding (creates user, exchanges auth token)
- Configures MQTT integration (broker = `mosquitto` container hostname)
- Configures whatwatt integration (topic = `whatwatt/data`)
- Publishes MQTT messages directly to Mosquitto on `localhost:1883`
- Verifies sensor states via HA REST API

## Test classes

| Class | Tests | What it covers |
|---|---|---|
| `TestIntegrationSetup` | 4 | Integration loaded, all 27 sensors created, button created, sensors unavailable before MQTT data. |
| `TestMQTTDataFlow` | 6 | Partial payload, full payload (24+ sensors available), power rounding, tariff integer, invalid JSON resilience, missing `sys_id` ignored. |
| `TestReload` | 2 | Reload preserves integration, sensors work after reload. |
| `TestReconfigure` | 3 | Duplicate topic rejected, invalid topic rejected, reconfigure changes topic (skipped - WebSocket only, covered by unit tests). |

**Total: 15 E2E tests (1 conditional skip)**

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `HA_URL` | `http://localhost:8123` | Home Assistant URL |
| `MQTT_BROKER` | `localhost` | Mosquitto host (for test runner) |
| `MQTT_PORT` | `1883` | Mosquitto port |
| `MQTT_BROKER_HA` | `mosquitto` | Mosquitto host (as seen by HA container, Docker network name) |

## CI matrix

E2E tests run in GitHub Actions against multiple HA versions:

| Version | Purpose |
|---|---|
| `stable` | Latest stable release |
| `2025.1` | Intermediate version |
| `2024.11` | Minimum supported version (requires `_get_reconfigure_entry()`) |

## Important notes

- **Fresh state required**: Each test run needs a clean HA instance. `run.sh` handles this with `docker compose down -v`. If you get "HA already onboarded" errors, restart with clean volumes.
- **Reconfigure test skip**: `test_reconfigure_changes_topic` is skipped because HA exposes reconfigure only via WebSocket API, not REST. Full reconfigure coverage is in `tests/test_config_flow.py`.
- **Polling pattern**: Tests use `_poll_sensor_state()` with timeout instead of `time.sleep()` to avoid flaky timing issues.
- **Separate venv**: E2E tests use their own `e2e/.venv` to avoid `pytest-socket` blocking from the HA test framework.
