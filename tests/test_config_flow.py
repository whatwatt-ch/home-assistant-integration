"""Tests for whatwatt config flow."""
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.whatwatt.const import CONF_DEVICE_IP, CONF_MQTT_TOPIC, DOMAIN


async def test_user_flow_success(
    hass: HomeAssistant,
    mqtt_mock,
) -> None:
    """Test successful user config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_MQTT_TOPIC: "whatwatt/data",
            CONF_DEVICE_IP: "192.168.1.100",
            "name": "My whatwatt",
        },
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "My whatwatt"
    assert result["data"][CONF_MQTT_TOPIC] == "whatwatt/data"
    assert result["data"][CONF_DEVICE_IP] == "192.168.1.100"


async def test_user_flow_without_ip(
    hass: HomeAssistant,
    mqtt_mock,
) -> None:
    """Test config flow without device IP."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_MQTT_TOPIC: "energy/whatwatt/go",
            CONF_DEVICE_IP: "",
            "name": "whatwatt",
        },
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"][CONF_DEVICE_IP] == ""


async def test_user_flow_invalid_topic_wildcard(
    hass: HomeAssistant,
    mqtt_mock,
) -> None:
    """Test config flow rejects MQTT topic with wildcard."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_MQTT_TOPIC: "whatwatt/#/data",
            CONF_DEVICE_IP: "",
            "name": "whatwatt",
        },
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"][CONF_MQTT_TOPIC] == "invalid_mqtt_topic"


async def test_user_flow_invalid_topic_empty(
    hass: HomeAssistant,
    mqtt_mock,
) -> None:
    """Test config flow rejects empty MQTT topic."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_MQTT_TOPIC: "",
            CONF_DEVICE_IP: "",
            "name": "whatwatt",
        },
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"][CONF_MQTT_TOPIC] == "invalid_mqtt_topic"


async def test_user_flow_invalid_ip(
    hass: HomeAssistant,
    mqtt_mock,
) -> None:
    """Test config flow rejects invalid IP address."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_MQTT_TOPIC: "whatwatt/data",
            CONF_DEVICE_IP: "999.999.999.999",
            "name": "whatwatt",
        },
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"][CONF_DEVICE_IP] == "invalid_ip"


async def test_user_flow_duplicate_topic(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test config flow aborts on duplicate MQTT topic."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_MQTT_TOPIC: "whatwatt/data",
            CONF_DEVICE_IP: "192.168.1.200",
            "name": "whatwatt 2",
        },
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_reconfigure_flow(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test reconfigure flow updates entry data."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    result = await mock_config_entry.start_reconfigure_flow(hass)
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reconfigure"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_MQTT_TOPIC: "whatwatt/new_topic",
            CONF_DEVICE_IP: "10.0.0.50",
            "name": "whatwatt updated",
        },
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reconfigure_successful"

    assert mock_config_entry.data[CONF_MQTT_TOPIC] == "whatwatt/new_topic"
    assert mock_config_entry.data[CONF_DEVICE_IP] == "10.0.0.50"


async def test_reconfigure_flow_invalid_ip(
    hass: HomeAssistant,
    mqtt_mock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test reconfigure flow rejects invalid IP."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    result = await mock_config_entry.start_reconfigure_flow(hass)

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_MQTT_TOPIC: "whatwatt/data",
            CONF_DEVICE_IP: "not.an.ip.address",
            "name": "whatwatt",
        },
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"][CONF_DEVICE_IP] == "invalid_ip"
