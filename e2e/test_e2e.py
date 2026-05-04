"""End-to-end tests for whatwatt Home Assistant integration.

Requires running services: Home Assistant + Mosquitto (see docker-compose.yml).
"""
import json
import os
import time

import paho.mqtt.publish as mqtt_publish
import pytest
import requests

HA_URL = os.environ.get("HA_URL", "http://localhost:8123")
MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_TOPIC = "whatwatt/data"

FULL_PAYLOAD = {
    "sys_id": "whatwatt-E2E-001",
    "meter_id": "MTR-E2E",
    "time": "2025-03-27T22:00:00Z",
    "power_in": 1.234,
    "power_out": 0.567,
    "power_in_l1": 0.45,
    "power_in_l2": 0.38,
    "power_in_l3": 0.40,
    "energy_in": 12345.6,
    "energy_out": 123.4,
    "energy_in_t1": 8234.2,
    "energy_in_t2": 4111.4,
    "energy_out_t1": 82.1,
    "energy_out_t2": 41.3,
    "voltage_l1": 230.1,
    "voltage_l2": 231.2,
    "voltage_l3": 229.8,
    "current_l1": 1.96,
    "current_l2": 1.65,
    "current_l3": 1.74,
    "power_factor": 0.98,
    "apparent_power": 1.26,
    "reactive_power_in": 0.25,
    "reactive_power_out": 0.0,
    "reactive_energy_in": 456.7,
    "reactive_energy_out": 12.3,
    "tariff": 2,
}

EXPECTED_SENSOR_COUNT = 27
POLL_INTERVAL = 0.3
POLL_TIMEOUT = 10


# ── Helpers ─────────────────────────────────────────────────────────


def _wait_for_ha():
    for _ in range(90):
        try:
            r = requests.get(f"{HA_URL}/api/onboarding", timeout=5)
            if r.status_code == 200:
                return
        except requests.ConnectionError:
            pass
        time.sleep(2)
    pytest.fail("Home Assistant did not start within 3 minutes")


def _onboard_ha():
    resp = requests.post(
        f"{HA_URL}/api/onboarding/users",
        json={
            "client_id": HA_URL,
            "name": "E2E Test",
            "username": "test",
            "password": "testpass1234",
            "language": "en",
        },
    )
    if resp.status_code in (400, 403) and "already" in resp.text.lower():
        pytest.fail(
            "HA already onboarded. Restart with fresh state: "
            "docker compose -f e2e/docker-compose.yml down -v && "
            "docker compose -f e2e/docker-compose.yml up -d"
        )
    assert resp.status_code == 200, f"Onboarding failed: {resp.text}"
    auth_code = resp.json()["auth_code"]

    resp = requests.post(
        f"{HA_URL}/auth/token",
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "client_id": HA_URL,
        },
    )
    assert resp.status_code == 200, f"Token exchange failed: {resp.text}"
    token = resp.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    requests.post(f"{HA_URL}/api/onboarding/core_config", headers=headers)
    requests.post(f"{HA_URL}/api/onboarding/analytics", headers=headers)
    requests.post(f"{HA_URL}/api/onboarding/integration", headers=headers)

    return token


def _make_headers(token):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _complete_config_flow(headers, handler, user_input):
    resp = requests.post(
        f"{HA_URL}/api/config/config_entries/flow",
        headers=headers,
        json={"handler": handler},
    )
    assert resp.status_code == 200, f"Failed to start {handler} flow: {resp.text}"
    flow = resp.json()
    flow_id = flow["flow_id"]

    if flow.get("type") == "form":
        resp = requests.post(
            f"{HA_URL}/api/config/config_entries/flow/{flow_id}",
            headers=headers,
            json=user_input,
        )
        assert resp.status_code == 200, f"Failed to configure {handler}: {resp.text}"
        return resp.json()

    return flow


def _publish_mqtt(payload, topic=MQTT_TOPIC):
    mqtt_publish.single(
        topic,
        json.dumps(payload),
        hostname=MQTT_BROKER,
        port=MQTT_PORT,
    )


def _get_states(headers):
    resp = requests.get(f"{HA_URL}/api/states", headers=headers)
    assert resp.status_code == 200
    return {s["entity_id"]: s for s in resp.json()}


def _get_whatwatt_sensors(headers):
    states = _get_states(headers)
    return {
        eid: s
        for eid, s in states.items()
        if eid.startswith("sensor.") and "whatwatt" in eid
    }


def _find_sensor(headers, fragment):
    """Find a single whatwatt sensor by entity_id fragment."""
    sensors = _get_whatwatt_sensors(headers)
    matches = [
        (eid, s) for eid, s in sensors.items() if fragment in eid
    ]
    assert matches, f"No sensor matching '{fragment}'"
    return matches[0]


def _poll_sensor_state(headers, fragment, expected, timeout=POLL_TIMEOUT):
    """Poll until a sensor reaches expected state. Returns the state dict."""
    deadline = time.monotonic() + timeout
    last_state = None
    while time.monotonic() < deadline:
        _, sensor = _find_sensor(headers, fragment)
        last_state = sensor["state"]
        if last_state == expected:
            return sensor
        time.sleep(POLL_INTERVAL)
    pytest.fail(
        f"Sensor '{fragment}' did not reach state '{expected}' "
        f"within {timeout}s (last: '{last_state}')"
    )


def _poll_sensor_not_state(headers, fragment, not_expected, timeout=POLL_TIMEOUT):
    """Poll until a sensor is NOT in the given state."""
    deadline = time.monotonic() + timeout
    last_state = None
    while time.monotonic() < deadline:
        _, sensor = _find_sensor(headers, fragment)
        last_state = sensor["state"]
        if last_state != not_expected:
            return sensor
        time.sleep(POLL_INTERVAL)
    pytest.fail(
        f"Sensor '{fragment}' still in state '{not_expected}' after {timeout}s"
    )


def _get_whatwatt_entry(headers):
    """Get the whatwatt config entry."""
    resp = requests.get(
        f"{HA_URL}/api/config/config_entries/entry", headers=headers
    )
    entries = [e for e in resp.json() if e["domain"] == "whatwatt"]
    assert entries, "No whatwatt config entry found"
    return entries[0]


# ── Session-scoped fixtures ────────────────────────────────────────


@pytest.fixture(scope="session")
def ha_headers():
    _wait_for_ha()
    token = _onboard_ha()
    return _make_headers(token)


@pytest.fixture(scope="session")
def mqtt_integration(ha_headers):
    broker_host = os.environ.get("MQTT_BROKER_HA", "mosquitto")
    result = _complete_config_flow(
        ha_headers,
        "mqtt",
        {"broker": broker_host, "port": 1883},
    )
    assert result.get("type") == "create_entry", f"MQTT setup failed: {result}"
    time.sleep(2)
    return result


@pytest.fixture(scope="session")
def whatwatt_integration(ha_headers, mqtt_integration):
    result = _complete_config_flow(
        ha_headers,
        "whatwatt",
        {"mqtt_topic": MQTT_TOPIC, "device_ip": "", "name": "whatwatt"},
    )
    assert result.get("type") == "create_entry", f"whatwatt setup failed: {result}"
    time.sleep(2)
    return result


# ── Tests: Setup ────────────────────────────────────────────────────


class TestIntegrationSetup:
    def test_whatwatt_loaded(self, ha_headers, whatwatt_integration):
        entry = _get_whatwatt_entry(ha_headers)
        assert entry["state"] == "loaded"

    def test_all_sensors_created(self, ha_headers, whatwatt_integration):
        sensors = _get_whatwatt_sensors(ha_headers)
        assert len(sensors) >= EXPECTED_SENSOR_COUNT, (
            f"Expected {EXPECTED_SENSOR_COUNT} sensors, got {len(sensors)}: "
            f"{sorted(sensors.keys())}"
        )

    def test_button_created(self, ha_headers, whatwatt_integration):
        states = _get_states(ha_headers)
        buttons = [
            eid for eid in states if eid.startswith("button.") and "whatwatt" in eid
        ]
        assert len(buttons) >= 1

    def test_sensors_unavailable_before_mqtt(self, ha_headers, whatwatt_integration):
        sensors = _get_whatwatt_sensors(ha_headers)
        for eid, state in sensors.items():
            assert state["state"] in ("unavailable", "unknown"), (
                f"{eid} should be unavailable before MQTT data, got: {state['state']}"
            )


# ── Tests: MQTT data flow ──────────────────────────────────────────


class TestMQTTDataFlow:
    def test_partial_payload_updates_matching_sensors(
        self, ha_headers, whatwatt_integration
    ):
        _publish_mqtt({"sys_id": "test", "voltage_l1": 232.5})
        sensor = _poll_sensor_not_state(ha_headers, "voltage_l1", "unavailable")
        assert float(sensor["state"]) == pytest.approx(232.5, abs=0.1)

    def test_full_payload_updates_all_sensors(
        self, ha_headers, whatwatt_integration
    ):
        _publish_mqtt(FULL_PAYLOAD)
        _poll_sensor_state(ha_headers, "tariff", "2")

        sensors = _get_whatwatt_sensors(ha_headers)
        available = [
            eid
            for eid, s in sensors.items()
            if s["state"] not in ("unavailable", "unknown")
        ]
        assert len(available) >= 24, (
            f"Expected most sensors available, got {len(available)}/{len(sensors)}"
        )

    def test_power_in_value_rounded(self, ha_headers, whatwatt_integration):
        _publish_mqtt({"sys_id": "test", "power_in": 3.456})
        sensor = _poll_sensor_state(ha_headers, "whatwatt_power_in", "3.46")
        assert float(sensor["state"]) == pytest.approx(3.46, abs=0.01)

    def test_tariff_is_integer(self, ha_headers, whatwatt_integration):
        _publish_mqtt({"sys_id": "test", "tariff": 3})
        sensor = _poll_sensor_state(ha_headers, "tariff", "3")
        assert sensor["state"] == "3"

    def test_invalid_json_does_not_crash(self, ha_headers, whatwatt_integration):
        mqtt_publish.single(
            MQTT_TOPIC, "not valid json{{{",
            hostname=MQTT_BROKER, port=MQTT_PORT,
        )
        time.sleep(1)
        entry = _get_whatwatt_entry(ha_headers)
        assert entry["state"] == "loaded"

    def test_missing_sys_id_ignored(self, ha_headers, whatwatt_integration):
        _publish_mqtt({"sys_id": "test", "power_in": 9.99})
        _poll_sensor_state(ha_headers, "whatwatt_power_in", "9.99")

        _publish_mqtt({"power_in": 0.01})
        time.sleep(1)

        _, sensor = _find_sensor(ha_headers, "whatwatt_power_in")
        assert float(sensor["state"]) == pytest.approx(9.99, abs=0.01)


# ── Tests: Reload / Unload ─────────────────────────────────────────


class TestReload:
    def test_reload_preserves_integration(self, ha_headers, whatwatt_integration):
        """Test that unloading and reloading the integration works."""
        entry = _get_whatwatt_entry(ha_headers)
        entry_id = entry["entry_id"]

        resp = requests.post(
            f"{HA_URL}/api/config/config_entries/entry/{entry_id}/reload",
            headers=ha_headers,
        )
        assert resp.status_code == 200

        deadline = time.monotonic() + POLL_TIMEOUT
        while time.monotonic() < deadline:
            entry = _get_whatwatt_entry(ha_headers)
            if entry["state"] == "loaded":
                break
            time.sleep(POLL_INTERVAL)
        assert entry["state"] == "loaded"

    def test_sensors_work_after_reload(self, ha_headers, whatwatt_integration):
        """Test that sensors still receive MQTT data after reload."""
        entry = _get_whatwatt_entry(ha_headers)
        requests.post(
            f"{HA_URL}/api/config/config_entries/entry/{entry['entry_id']}/reload",
            headers=ha_headers,
        )
        deadline = time.monotonic() + POLL_TIMEOUT
        while time.monotonic() < deadline:
            if _get_whatwatt_entry(ha_headers)["state"] == "loaded":
                break
            time.sleep(POLL_INTERVAL)

        _publish_mqtt({"sys_id": "test", "power_in": 7.77})
        sensor = _poll_sensor_state(ha_headers, "whatwatt_power_in", "7.77")
        assert float(sensor["state"]) == pytest.approx(7.77, abs=0.01)


# ── Tests: Reconfigure ─────────────────────────────────────────────


class TestReconfigure:
    def test_duplicate_topic_rejected(self, ha_headers, whatwatt_integration):
        result = _complete_config_flow(
            ha_headers,
            "whatwatt",
            {"mqtt_topic": MQTT_TOPIC, "device_ip": "", "name": "whatwatt 2"},
        )
        assert result.get("type") == "abort"
        assert result.get("reason") == "already_configured"

    def test_invalid_topic_rejected(self, ha_headers, whatwatt_integration):
        resp = requests.post(
            f"{HA_URL}/api/config/config_entries/flow",
            headers=ha_headers,
            json={"handler": "whatwatt"},
        )
        flow_id = resp.json()["flow_id"]

        resp = requests.post(
            f"{HA_URL}/api/config/config_entries/flow/{flow_id}",
            headers=ha_headers,
            json={"mqtt_topic": "topic/#/bad", "device_ip": "", "name": "test"},
        )
        result = resp.json()
        assert result.get("type") == "form"
        assert "mqtt_topic" in result.get("errors", {})

    def test_reconfigure_changes_topic(self, ha_headers, whatwatt_integration):
        """Test reconfigure via REST API (HA 2024.11+)."""
        entry = _get_whatwatt_entry(ha_headers)
        entry_id = entry["entry_id"]

        resp = requests.post(
            f"{HA_URL}/api/config/config_entries/entry/{entry_id}/reconfigure",
            headers=ha_headers,
        )
        if resp.status_code == 404:
            pytest.skip("Reconfigure REST endpoint not available in this HA version")

        assert resp.status_code == 200
        flow_id = resp.json()["flow_id"]

        new_topic = "whatwatt/e2e_new"
        resp = requests.post(
            f"{HA_URL}/api/config/config_entries/flow/{flow_id}",
            headers=ha_headers,
            json={"mqtt_topic": new_topic, "device_ip": "", "name": "whatwatt"},
        )
        result = resp.json()
        assert result.get("type") == "abort"
        assert result.get("reason") == "reconfigure_successful"

        deadline = time.monotonic() + POLL_TIMEOUT
        while time.monotonic() < deadline:
            if _get_whatwatt_entry(ha_headers)["state"] == "loaded":
                break
            time.sleep(POLL_INTERVAL)

        _publish_mqtt({"sys_id": "test", "power_in": 5.55}, topic=new_topic)
        sensor = _poll_sensor_state(ha_headers, "whatwatt_power_in", "5.55")
        assert float(sensor["state"]) == pytest.approx(5.55, abs=0.01)

        # Restore original topic
        resp = requests.post(
            f"{HA_URL}/api/config/config_entries/entry/{entry_id}/reconfigure",
            headers=ha_headers,
        )
        flow_id = resp.json()["flow_id"]
        requests.post(
            f"{HA_URL}/api/config/config_entries/flow/{flow_id}",
            headers=ha_headers,
            json={"mqtt_topic": MQTT_TOPIC, "device_ip": "", "name": "whatwatt"},
        )
        time.sleep(2)
