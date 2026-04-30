"""The whatwatt integration."""
import json
import logging

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN,
    CONF_MQTT_TOPIC,
    CONF_DEVICE_IP,
    DEFAULT_NAME,
    ATTR_SYS_ID,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR, Platform.BUTTON]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the whatwatt component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up whatwatt from a config entry."""
    mqtt_topic = entry.data[CONF_MQTT_TOPIC]
    device_ip = entry.data.get(CONF_DEVICE_IP, "")
    name = entry.data.get("name", DEFAULT_NAME)

    if not hass.services.has_service("mqtt", "publish"):
        _LOGGER.error("MQTT integration is not set up")
        raise ConfigEntryNotReady("MQTT integration is not set up")

    device_info = DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name=name,
        manufacturer="whatwatt AG",
        model="whatwatt Go",
        configuration_url=f"http://{device_ip}" if device_ip else None,
    )

    hass.data[DOMAIN][entry.entry_id] = {
        "mqtt_topic": mqtt_topic,
        "device_ip": device_ip,
        "device_info": device_info,
        "sensors": {},
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    @callback
    def message_received(msg):
        """Handle new MQTT messages."""
        try:
            payload = json.loads(msg.payload)
            _LOGGER.debug("whatwatt: received message: %s", payload)

            sys_id = payload.get(ATTR_SYS_ID)
            if not sys_id:
                _LOGGER.warning("whatwatt: message missing sys_id field: %s", payload)
                return

            entry_data = hass.data.get(DOMAIN, {}).get(entry.entry_id)
            if not entry_data:
                return

            for sensor in entry_data.get("sensors", {}).values():
                sensor.handle_mqtt_message(payload)

        except json.JSONDecodeError:
            _LOGGER.error("whatwatt: invalid JSON in MQTT message")
        except Exception as ex:
            _LOGGER.error("whatwatt: error processing MQTT message: %s", ex)

    unsubscribe = await mqtt.async_subscribe(hass, mqtt_topic, message_received)

    entry.async_on_unload(unsubscribe)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
