"""Tests for whatwatt button platform."""
from homeassistant.core import HomeAssistant

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.whatwatt.const import DOMAIN


async def test_button_created(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that the configuration button is created."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    states = hass.states.async_all("button")
    assert len(states) == 1


async def test_button_press(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that pressing the button does not crash."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    states = hass.states.async_all("button")
    entity_id = states[0].entity_id

    await hass.services.async_call(
        "button",
        "press",
        {"entity_id": entity_id},
        blocking=True,
    )
