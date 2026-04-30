"""Sensor platform for whatwatt integration."""
import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the whatwatt sensor platform."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    device_info = entry_data["device_info"]

    sensors = []
    for sensor_type, sensor_config in SENSOR_TYPES.items():
        sensor = WhatWattSensor(
            config_entry.entry_id,
            device_info,
            sensor_type,
            sensor_config,
        )
        sensors.append(sensor)
        entry_data["sensors"][sensor_type] = sensor

    async_add_entities(sensors)


class WhatWattSensor(SensorEntity):
    """Representation of a whatwatt sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        entry_id: str,
        device_info: Any,
        sensor_type: str,
        sensor_config: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        self._sensor_type = sensor_type
        self._state = None
        self._available = False

        self._attr_unique_id = f"{entry_id}_{sensor_type}"
        self._attr_translation_key = sensor_type
        self._attr_device_info = device_info
        self._attr_native_unit_of_measurement = sensor_config.get("unit")
        self._attr_icon = sensor_config.get("icon")
        self._attr_device_class = sensor_config.get("device_class")
        self._attr_state_class = sensor_config.get("state_class")

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self._state

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @callback
    def handle_mqtt_message(self, message: Dict[str, Any]) -> None:
        """Handle new MQTT messages."""
        if self._sensor_type in message:
            value = message[self._sensor_type]
            if value is None:
                return
            try:
                if self._sensor_type == "tariff":
                    self._state = int(value)
                else:
                    self._state = round(float(value), 2)
                self._available = True
            except (ValueError, TypeError) as ex:
                _LOGGER.error(
                    "whatwatt: could not parse %s value %s: %s",
                    self._sensor_type,
                    value,
                    ex,
                )
                self._state = None
                self._available = False

            self.async_write_ha_state()
