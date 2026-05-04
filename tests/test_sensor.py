"""Tests for whatwatt sensor platform."""
import json

import pytest
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
)
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


# ── State machine tests ─────────────────────────────────────────────


async def test_state_machine_updated_on_mqtt(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that MQTT messages update the HA state machine, not just native_value."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    payload = {"sys_id": "test", "power_in": 2.345, "voltage_l1": 231.5, "tariff": 1}
    async_fire_mqtt_message(hass, "whatwatt/data", json.dumps(payload))
    await hass.async_block_till_done()

    power_state = hass.states.get("sensor.whatwatt_power_in")
    assert power_state is not None
    assert float(power_state.state) == 2.35

    voltage_state = hass.states.get("sensor.whatwatt_voltage_l1")
    assert voltage_state is not None
    assert float(voltage_state.state) == 231.5

    tariff_state = hass.states.get("sensor.whatwatt_tariff")
    assert tariff_state is not None
    assert tariff_state.state == "1"


async def test_state_machine_unavailable_before_data(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that sensors show as unavailable in state machine before MQTT data."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    state = hass.states.get("sensor.whatwatt_power_in")
    assert state is not None
    assert state.state == "unavailable"


async def test_state_machine_transitions_to_unavailable(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that invalid value transitions state to unavailable."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    payload = {"sys_id": "test", "power_in": 1.5}
    async_fire_mqtt_message(hass, "whatwatt/data", json.dumps(payload))
    await hass.async_block_till_done()
    assert hass.states.get("sensor.whatwatt_power_in").state == "1.5"

    payload = {"sys_id": "test", "power_in": "garbage"}
    async_fire_mqtt_message(hass, "whatwatt/data", json.dumps(payload))
    await hass.async_block_till_done()
    assert hass.states.get("sensor.whatwatt_power_in").state == "unavailable"


async def test_state_machine_full_payload(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
    sample_mqtt_payload: dict,
) -> None:
    """Test that all sensors appear in state machine after full payload."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    async_fire_mqtt_message(hass, "whatwatt/data", json.dumps(sample_mqtt_payload))
    await hass.async_block_till_done()

    all_states = hass.states.async_all("sensor")
    whatwatt_states = [s for s in all_states if "whatwatt" in s.entity_id]
    available = [s for s in whatwatt_states if s.state != "unavailable"]
    assert len(whatwatt_states) == len(SENSOR_TYPES)
    assert len(available) >= 24


# ── Entity attribute tests ──────────────────────────────────────────


@pytest.mark.parametrize(
    "sensor_key,expected_device_class,expected_state_class,expected_unit",
    [
        ("power_in", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT, UnitOfPower.KILO_WATT),
        ("power_out", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT, UnitOfPower.KILO_WATT),
        ("energy_in", SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING, UnitOfEnergy.KILO_WATT_HOUR),
        ("energy_out", SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING, UnitOfEnergy.KILO_WATT_HOUR),
        ("voltage_l1", SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT, UnitOfElectricPotential.VOLT),
        ("current_l1", SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT, UnitOfElectricCurrent.AMPERE),
        ("power_factor", SensorDeviceClass.POWER_FACTOR, SensorStateClass.MEASUREMENT, None),
    ],
)
async def test_sensor_attributes(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
    sensor_key: str,
    expected_device_class: SensorDeviceClass | None,
    expected_state_class: SensorStateClass | None,
    expected_unit: str | None,
) -> None:
    """Test that sensor attributes match const.py definitions."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    sensor = hass.data[DOMAIN][mock_config_entry.entry_id]["sensors"][sensor_key]
    assert sensor.device_class == expected_device_class
    assert sensor.state_class == expected_state_class
    assert sensor.native_unit_of_measurement == expected_unit


async def test_sensor_attributes_custom_units(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test sensors with custom units (no HA device_class)."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    sensors = hass.data[DOMAIN][mock_config_entry.entry_id]["sensors"]

    assert sensors["apparent_power"].native_unit_of_measurement == "kVA"
    assert sensors["apparent_power"].state_class == SensorStateClass.MEASUREMENT

    assert sensors["reactive_power_in"].native_unit_of_measurement == "kvar"
    assert sensors["reactive_energy_in"].native_unit_of_measurement == "kvarh"
    assert sensors["reactive_energy_in"].state_class == SensorStateClass.TOTAL_INCREASING

    assert sensors["tariff"].native_unit_of_measurement is None


async def test_sensor_precision(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test suggested_display_precision matches const.py config."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    sensors = hass.data[DOMAIN][mock_config_entry.entry_id]["sensors"]

    assert sensors["power_in"].suggested_display_precision == 2
    assert sensors["energy_in"].suggested_display_precision == 1
    assert sensors["voltage_l1"].suggested_display_precision == 1
    assert sensors["current_l1"].suggested_display_precision == 2
    assert sensors["tariff"].suggested_display_precision == 0


async def test_sensor_unique_ids(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that all sensors have unique IDs."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    sensors = hass.data[DOMAIN][mock_config_entry.entry_id]["sensors"]
    unique_ids = [s.unique_id for s in sensors.values()]
    assert len(unique_ids) == len(set(unique_ids))
    for uid in unique_ids:
        assert uid.startswith(mock_config_entry.entry_id)
