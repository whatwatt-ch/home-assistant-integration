"""Config flow for whatwatt integration."""
import re
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult

from .const import (
    CONF_DEVICE_IP,
    CONF_MQTT_TOPIC,
    DEFAULT_NAME,
    DOMAIN,
)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_MQTT_TOPIC): str,
        vol.Optional(CONF_DEVICE_IP, default=""): str,
        vol.Optional("name", default=DEFAULT_NAME): str,
    }
)


class WhatWattConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for whatwatt."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if not self.hass.services.has_service("mqtt", "publish"):
            errors["base"] = "mqtt_not_configured"
            return self.async_show_form(
                step_id="user",
                data_schema=DATA_SCHEMA,
                errors=errors,
                description_placeholders={
                    "mqtt_config_url": "/config/integrations/integration/mqtt"
                },
            )

        if user_input is not None:
            errors = self._validate_input(user_input)

            if not errors:
                await self.async_set_unique_id(user_input[CONF_MQTT_TOPIC])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input.get("name", DEFAULT_NAME),
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle reconfiguration."""
        errors: dict[str, str] = {}
        entry = self._get_reconfigure_entry()

        if user_input is not None:
            errors = self._validate_input(user_input)

            if not errors:
                return self.async_update_reload_and_abort(
                    entry,
                    data_updates=user_input,
                    unique_id=user_input[CONF_MQTT_TOPIC],
                )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=self.add_suggested_values_to_schema(
                DATA_SCHEMA, entry.data
            ),
            errors=errors,
        )

    @staticmethod
    def _validate_input(user_input: dict[str, Any]) -> dict[str, str]:
        """Validate user input."""
        errors: dict[str, str] = {}

        mqtt_topic = user_input.get(CONF_MQTT_TOPIC)
        if not mqtt_topic or not WhatWattConfigFlow._is_valid_mqtt_topic(mqtt_topic):
            errors[CONF_MQTT_TOPIC] = "invalid_mqtt_topic"

        device_ip = user_input.get(CONF_DEVICE_IP, "")
        if device_ip and not WhatWattConfigFlow._is_valid_ip(device_ip):
            errors[CONF_DEVICE_IP] = "invalid_ip"

        return errors

    @staticmethod
    def _is_valid_mqtt_topic(topic: str) -> bool:
        """Validate MQTT topic format."""
        return isinstance(topic, str) and len(topic) > 0 and "#" not in topic and "+" not in topic

    @staticmethod
    def _is_valid_ip(ip: str) -> bool:
        """Validate IP address format."""
        ip_pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
        match = re.match(ip_pattern, ip)
        if not match:
            return False
        return all(int(octet) <= 255 for octet in match.groups())
