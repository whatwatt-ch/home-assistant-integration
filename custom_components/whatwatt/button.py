"""Button platform for WhatWatt integration."""
import logging
from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_DEVICE_IP

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the WhatWatt button."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    device_ip = config_entry.data.get(CONF_DEVICE_IP, "")
    device_info = entry_data["device_info"]

    async_add_entities([WhatWattConfigButton(config_entry.entry_id, device_ip, device_info)])


class WhatWattConfigButton(ButtonEntity):
    """Button to open the WhatWatt configuration page."""

    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.CONFIG
    _attr_icon = "mdi:cog"
    _attr_translation_key = "configuration"

    def __init__(self, entry_id: str, device_ip: str, device_info: Any) -> None:
        """Initialize the button entity."""
        self._device_ip = device_ip
        self._attr_unique_id = f"{entry_id}_config"
        self._attr_device_info = device_info

    def press(self) -> None:
        """Handle the button press."""
        _LOGGER.info(
            "WhatWatt: configuration page available at http://%s", self._device_ip
        )
