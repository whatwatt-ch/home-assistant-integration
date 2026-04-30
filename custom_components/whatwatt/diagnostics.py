"""Diagnostics for whatwatt integration."""
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    entry_data = hass.data.get(DOMAIN, {}).get(entry.entry_id, {})

    sensors_diag = {}
    for key, sensor in entry_data.get("sensors", {}).items():
        sensors_diag[key] = {
            "state": sensor.native_value,
            "available": sensor.available,
            "unit": str(sensor.native_unit_of_measurement),
        }

    return {
        "config_entry_data": dict(entry.data),
        "sensor_count": len(sensors_diag),
        "sensors": sensors_diag,
    }
