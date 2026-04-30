"""Constants for the whatwatt integration."""

DOMAIN = "whatwatt"

# Configuration
CONF_MQTT_TOPIC = "mqtt_topic"
CONF_DEVICE_IP = "device_ip"

# Default values
DEFAULT_NAME = "whatwatt"

# Attributes
ATTR_SYS_ID = "sys_id"
ATTR_METER_ID = "meter_id"
ATTR_TIME = "time"
ATTR_POWER_IN = "power_in"
ATTR_POWER_OUT = "power_out"
ATTR_ENERGY_IN = "energy_in"
ATTR_ENERGY_OUT = "energy_out"
ATTR_VOLTAGE_L1 = "voltage_l1"
ATTR_VOLTAGE_L2 = "voltage_l2"
ATTR_VOLTAGE_L3 = "voltage_l3"

# Units
UNIT_POWER = "kW"
UNIT_ENERGY = "kWh"
UNIT_VOLTAGE = "V"

# Sensor types
SENSOR_TYPES = {
    ATTR_POWER_IN: {
        "name": "Power In",
        "unit": UNIT_POWER,
        "icon": "mdi:transmission-tower-import",
        "device_class": "power",
        "state_class": "measurement",
    },
    ATTR_POWER_OUT: {
        "name": "Power Out",
        "unit": UNIT_POWER,
        "icon": "mdi:transmission-tower-export",
        "device_class": "power",
        "state_class": "measurement",
    },
    ATTR_ENERGY_IN: {
        "name": "Energy In",
        "unit": UNIT_ENERGY,
        "icon": "mdi:home-import-outline",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    ATTR_ENERGY_OUT: {
        "name": "Energy Out",
        "unit": UNIT_ENERGY,
        "icon": "mdi:home-export-outline",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    ATTR_VOLTAGE_L1: {
        "name": "Voltage L1",
        "unit": UNIT_VOLTAGE,
        "icon": "mdi:sine-wave",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    ATTR_VOLTAGE_L2: {
        "name": "Voltage L2",
        "unit": UNIT_VOLTAGE,
        "icon": "mdi:sine-wave",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    ATTR_VOLTAGE_L3: {
        "name": "Voltage L3",
        "unit": UNIT_VOLTAGE,
        "icon": "mdi:sine-wave",
        "device_class": "voltage",
        "state_class": "measurement",
    },
}
