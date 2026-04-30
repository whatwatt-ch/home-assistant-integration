"""Tests for whatwatt diagnostics."""
import json

from homeassistant.core import HomeAssistant

from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_fire_mqtt_message,
)

from custom_components.whatwatt.const import DOMAIN, CONF_MQTT_TOPIC, CONF_DEVICE_IP
from custom_components.whatwatt.diagnostics import async_get_config_entry_diagnostics


async def test_diagnostics(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
    sample_mqtt_payload: dict,
) -> None:
    """Test diagnostics returns expected data."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    async_fire_mqtt_message(hass, "whatwatt/data", json.dumps(sample_mqtt_payload))
    await hass.async_block_till_done()

    diag = await async_get_config_entry_diagnostics(hass, mock_config_entry)

    assert diag["config_entry_data"][CONF_MQTT_TOPIC] == "whatwatt/data"
    assert diag["config_entry_data"][CONF_DEVICE_IP] == "192.168.1.100"
    assert diag["sensor_count"] == 27
    assert diag["sensors"]["power_in"]["state"] == 1.23
    assert diag["sensors"]["power_in"]["available"] is True


async def test_diagnostics_no_data(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test diagnostics before any MQTT data received."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    diag = await async_get_config_entry_diagnostics(hass, mock_config_entry)

    assert diag["sensor_count"] == 27
    assert diag["sensors"]["power_in"]["state"] is None
    assert diag["sensors"]["power_in"]["available"] is False
