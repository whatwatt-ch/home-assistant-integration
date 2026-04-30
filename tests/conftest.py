"""Fixtures for whatwatt tests."""
import pytest

from homeassistant.core import HomeAssistant

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.whatwatt.const import DOMAIN, CONF_MQTT_TOPIC, CONF_DEVICE_IP


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations in all tests."""
    yield


@pytest.fixture(autouse=True)
async def cleanup_timers(hass: HomeAssistant):
    """Cancel lingering MQTT periodic timers after each test."""
    yield
    for handle in list(hass.loop._scheduled):
        if not handle.cancelled() and "misc_periodic" in str(handle):
            handle.cancel()


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Create a mock config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_MQTT_TOPIC: "whatwatt/data",
            CONF_DEVICE_IP: "192.168.1.100",
            "name": "whatwatt",
        },
        entry_id="test_entry_id",
        unique_id="whatwatt/data",
    )


@pytest.fixture
def mock_config_entry_no_ip() -> MockConfigEntry:
    """Create a mock config entry without device IP."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_MQTT_TOPIC: "whatwatt/data",
            CONF_DEVICE_IP: "",
            "name": "whatwatt",
        },
        entry_id="test_entry_no_ip",
        unique_id="whatwatt/data",
    )


@pytest.fixture
def sample_mqtt_payload() -> dict:
    """Return a sample MQTT payload."""
    return {
        "sys_id": "whatwatt-ABC123",
        "meter_id": "MTR001",
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
        "tariff": 1,
    }
