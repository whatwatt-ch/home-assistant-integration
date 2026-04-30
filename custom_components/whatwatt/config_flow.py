"""Config flow for whatwatt integration."""
import re
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType
from homeassistant.components import mqtt

from .const import (
    DOMAIN,
    CONF_MQTT_TOPIC,
    CONF_DEVICE_IP,
    DEFAULT_NAME,
)


class WhatWattConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for whatwatt."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        # Check if MQTT integration is set up
        if not self.hass.services.has_service("mqtt", "publish"):
            errors["base"] = "mqtt_not_configured"
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_MQTT_TOPIC): str,
                        vol.Required(CONF_DEVICE_IP): str,
                        vol.Optional("name", default=DEFAULT_NAME): str,
                    }
                ),
                errors=errors,
                description_placeholders={
                    "mqtt_config_url": "/config/integrations/integration/mqtt"
                }
            )

        if user_input is not None:
            # Validate MQTT topic
            mqtt_topic = user_input.get(CONF_MQTT_TOPIC)
            if not mqtt_topic or not self._is_valid_mqtt_topic(mqtt_topic):
                errors[CONF_MQTT_TOPIC] = "invalid_mqtt_topic"

            # Validate IP address
            device_ip = user_input.get(CONF_DEVICE_IP)
            if not device_ip or not self._is_valid_ip(device_ip):
                errors[CONF_DEVICE_IP] = "invalid_ip"

            if not errors:
                # Create unique ID from MQTT topic
                await self.async_set_unique_id(mqtt_topic)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input.get("name", DEFAULT_NAME),
                    data=user_input,
                )

        # Show form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_MQTT_TOPIC): str,
                    vol.Required(CONF_DEVICE_IP): str,
                    vol.Optional("name", default=DEFAULT_NAME): str,
                }
            ),
            errors=errors,
        )

    @staticmethod
    def _is_valid_mqtt_topic(topic):
        """Validate MQTT topic format."""
        # Basic validation - can be expanded as needed
        return isinstance(topic, str) and len(topic) > 0 and "#" not in topic and "+" not in topic

    @staticmethod
    def _is_valid_ip(ip):
        """Validate IP address format."""
        ip_pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
        match = re.match(ip_pattern, ip)
        if not match:
            return False
        
        # Check that each octet is between 0 and 255
        for octet in match.groups():
            if int(octet) > 255:
                return False
                
        return True
