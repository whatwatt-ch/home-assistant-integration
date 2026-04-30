"""Tests for whatwatt sensor platform."""
import json

from homeassistant.core import HomeAssistant

from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_fire_mqtt_message,
)

from custom_components.whatwatt.const import DOMAIN, SENSOR_TYPES


async def test_all_sensor_types_created(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that all sensor types are registered."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    entry_data = hass.data[DOMAIN][mock_config_entry.entry_id]
    assert len(entry_data["sensors"]) == len(SENSOR_TYPES)


async def test_sensor_power_rounding(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that power values are rounded to 2 decimal places."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    payload = {"sys_id": "test", "power_in": 1.23456}
    async_fire_mqtt_message(hass, "whatwatt/data", json.dumps(payload))
    await hass.async_block_till_done()

    sensor = hass.data[DOMAIN][mock_config_entry.entry_id]["sensors"]["power_in"]
    assert sensor.native_value == 1.23


async def test_sensor_tariff_integer(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that tariff is parsed as integer."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    payload = {"sys_id": "test", "tariff": 2}
    async_fire_mqtt_message(hass, "whatwatt/data", json.dumps(payload))
    await hass.async_block_till_done()

    sensor = hass.data[DOMAIN][mock_config_entry.entry_id]["sensors"]["tariff"]
    assert sensor.native_value == 2
    assert isinstance(sensor.native_value, int)


async def test_sensor_tariff_from_string(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that tariff is parsed correctly from string."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    payload = {"sys_id": "test", "tariff": "3"}
    async_fire_mqtt_message(hass, "whatwatt/data", json.dumps(payload))
    await hass.async_block_till_done()

    sensor = hass.data[DOMAIN][mock_config_entry.entry_id]["sensors"]["tariff"]
    assert sensor.native_value == 3
    assert isinstance(sensor.native_value, int)


async def test_sensor_null_value_ignored(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that null values from gateway are ignored."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    # First send a valid value
    payload = {"sys_id": "test", "power_in": 1.5}
    async_fire_mqtt_message(hass, "whatwatt/data", json.dumps(payload))
    await hass.async_block_till_done()

    sensor = hass.data[DOMAIN][mock_config_entry.entry_id]["sensors"]["power_in"]
    assert sensor.native_value == 1.5
    assert sensor.available is True

    # Now send null — state should NOT change
    payload = {"sys_id": "test", "power_in": None}
    async_fire_mqtt_message(hass, "whatwatt/data", json.dumps(payload))
    await hass.async_block_till_done()

    assert sensor.native_value == 1.5
    assert sensor.available is True


async def test_sensor_invalid_value(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that invalid values set sensor to unavailable."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    payload = {"sys_id": "test", "power_in": "not_a_number"}
    async_fire_mqtt_message(hass, "whatwatt/data", json.dumps(payload))
    await hass.async_block_till_done()

    sensor = hass.data[DOMAIN][mock_config_entry.entry_id]["sensors"]["power_in"]
    assert sensor.native_value is None
    assert sensor.available is False


async def test_sensor_partial_payload(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that partial payloads only update matching sensors."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    # Send only voltage
    payload = {"sys_id": "test", "voltage_l1": 230.5}
    async_fire_mqtt_message(hass, "whatwatt/data", json.dumps(payload))
    await hass.async_block_till_done()

    sensors = hass.data[DOMAIN][mock_config_entry.entry_id]["sensors"]
    assert sensors["voltage_l1"].native_value == 230.5
    assert sensors["voltage_l1"].available is True
    assert sensors["power_in"].available is False


async def test_sensor_all_values_update(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
    sample_mqtt_payload: dict,
) -> None:
    """Test that a full payload updates all sensors."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    async_fire_mqtt_message(hass, "whatwatt/data", json.dumps(sample_mqtt_payload))
    await hass.async_block_till_done()

    sensors = hass.data[DOMAIN][mock_config_entry.entry_id]["sensors"]

    assert sensors["power_in"].native_value == 1.23
    assert sensors["power_out"].native_value == 0.57
    assert sensors["voltage_l1"].native_value == 230.1
    assert sensors["current_l1"].native_value == 1.96
    assert sensors["power_factor"].native_value == 0.98
    assert sensors["apparent_power"].native_value == 1.26
    assert sensors["reactive_power_in"].native_value == 0.25
    assert sensors["energy_in"].native_value == 12345.6
    assert sensors["tariff"].native_value == 1
    assert isinstance(sensors["tariff"].native_value, int)

    for key in sample_mqtt_payload:
        if key in sensors:
            assert sensors[key].available is True
