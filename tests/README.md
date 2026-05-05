# Unit Tests

Unit tests run against a mocked Home Assistant instance using
[`pytest-homeassistant-custom-component`](https://github.com/MatthewFlamworthy/pytest-homeassistant-custom-component).
No Docker, network, or real HA installation is required.

## Running

```bash
pip install -e ".[test]"
pytest tests/ --tb=short -q
```

With coverage:

```bash
pytest tests/ --cov=custom_components/whatwatt --cov-report=term-missing --cov-fail-under=80
```

## Test modules

| Module | Tests | What it covers |
|---|---|---|
| `test_init.py` | 9 | Integration lifecycle: setup, unload, MQTT dispatch, invalid JSON, missing `sys_id`, setup without IP. Device registry: metadata, `configuration_url`, single-device constraint. |
| `test_sensor.py` | 21 | Sensor creation (all 27 types), value rounding (2dp for power), tariff parsing (int from int/string), null value handling, invalid value -> unavailable, partial payload. HA state machine verification. Entity attributes: `device_class`, `state_class`, `native_unit_of_measurement`, `suggested_display_precision`, unique IDs. |
| `test_config_flow.py` | 8 | User config flow: success, optional IP, invalid topic (wildcard/empty), invalid IP, duplicate topic abort. Reconfigure flow: topic+IP update, invalid IP rejection. |
| `test_button.py` | 2 | Configuration button creation and press (no crash). |
| `test_diagnostics.py` | 2 | Diagnostics output with data and before any MQTT data. |

**Total: 42 unit tests, coverage target >= 80% (actual ~97%)**

## Fixtures (conftest.py)

| Fixture | Scope | Description |
|---|---|---|
| `auto_enable_custom_integrations` | function (autouse) | Enables loading custom components in test HA instance. |
| `cleanup_timers` | function (autouse) | Cancels lingering MQTT periodic timers after each test to avoid `asyncio` warnings. |
| `mock_config_entry` | function | Config entry with topic `whatwatt/data`, IP `192.168.1.100`. |
| `mock_config_entry_no_ip` | function | Config entry without device IP (empty string). |
| `sample_mqtt_payload` | function | Full 27-field MQTT payload matching all `SENSOR_TYPES`. |

## Key patterns

- **State machine tests**: verify that `hass.states.get("sensor.whatwatt_*")` reflects actual entity state, not just `native_value` on the Python object.
- **Parametrized attribute tests**: `@pytest.mark.parametrize` covers `device_class`, `state_class`, and `unit` for representative sensor types.
- **Availability transitions**: tests verify sensors start as `unavailable`, become available on valid data, and return to `unavailable` on invalid data.
