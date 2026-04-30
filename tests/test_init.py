"""Tests for whatwatt integration setup."""
import json

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant

from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_fire_mqtt_message,
)

from custom_components.whatwatt.const import DOMAIN


async def test_setup_entry(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test setting up the integration creates entry data."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED
    assert DOMAIN in hass.data
    assert mock_config_entry.entry_id in hass.data[DOMAIN]
    assert "sensors" in hass.data[DOMAIN][mock_config_entry.entry_id]


async def test_unload_entry(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test unloading the integration cleans up entry data."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED
    assert mock_config_entry.entry_id not in hass.data.get(DOMAIN, {})


async def test_mqtt_message_dispatched_to_sensors(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
    sample_mqtt_payload: dict,
) -> None:
    """Test that MQTT messages reach sensors and update state."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    async_fire_mqtt_message(hass, "whatwatt/data", json.dumps(sample_mqtt_payload))
    await hass.async_block_till_done()

    entry_data = hass.data[DOMAIN][mock_config_entry.entry_id]
    power_sensor = entry_data["sensors"]["power_in"]
    assert power_sensor.available is True
    assert power_sensor.native_value == 1.23


async def test_mqtt_invalid_json(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that invalid JSON does not crash the integration."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    async_fire_mqtt_message(hass, "whatwatt/data", "not valid json{{{")
    await hass.async_block_till_done()

    entry_data = hass.data[DOMAIN][mock_config_entry.entry_id]
    power_sensor = entry_data["sensors"]["power_in"]
    assert power_sensor.available is False


async def test_mqtt_missing_sys_id(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that messages without sys_id are ignored."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    payload = {"power_in": 1.5}
    async_fire_mqtt_message(hass, "whatwatt/data", json.dumps(payload))
    await hass.async_block_till_done()

    entry_data = hass.data[DOMAIN][mock_config_entry.entry_id]
    power_sensor = entry_data["sensors"]["power_in"]
    assert power_sensor.available is False


async def test_setup_entry_no_ip(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry_no_ip: MockConfigEntry,
) -> None:
    """Test setup works without device IP."""
    mock_config_entry_no_ip.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry_no_ip.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry_no_ip.state is ConfigEntryState.LOADED
