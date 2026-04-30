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

# Active power (kW, scaler -3)
ATTR_POWER_IN = "power_in"
ATTR_POWER_OUT = "power_out"
ATTR_POWER_IN_L1 = "power_in_l1"
ATTR_POWER_IN_L2 = "power_in_l2"
ATTR_POWER_IN_L3 = "power_in_l3"
ATTR_POWER_OUT_L1 = "power_out_l1"
ATTR_POWER_OUT_L2 = "power_out_l2"
ATTR_POWER_OUT_L3 = "power_out_l3"

# Active energy (kWh, scaler -3)
ATTR_ENERGY_IN = "energy_in"
ATTR_ENERGY_OUT = "energy_out"
ATTR_ENERGY_IN_T1 = "energy_in_t1"
ATTR_ENERGY_IN_T2 = "energy_in_t2"
ATTR_ENERGY_OUT_T1 = "energy_out_t1"
ATTR_ENERGY_OUT_T2 = "energy_out_t2"

# Voltage (V, scaler 0)
ATTR_VOLTAGE_L1 = "voltage_l1"
ATTR_VOLTAGE_L2 = "voltage_l2"
ATTR_VOLTAGE_L3 = "voltage_l3"

# Current (A, scaler 0)
ATTR_CURRENT_L1 = "current_l1"
ATTR_CURRENT_L2 = "current_l2"
ATTR_CURRENT_L3 = "current_l3"

# Power factor (ratio 0-1, scaler 0)
ATTR_POWER_FACTOR = "power_factor"

# Apparent power (kVA, scaler -3)
ATTR_APPARENT_POWER = "apparent_power"

# Reactive power (kvar, scaler -3)
ATTR_REACTIVE_POWER_IN = "reactive_power_in"
ATTR_REACTIVE_POWER_OUT = "reactive_power_out"

# Reactive energy (kvarh, scaler -3)
ATTR_REACTIVE_ENERGY_IN = "reactive_energy_in"
ATTR_REACTIVE_ENERGY_OUT = "reactive_energy_out"

# Tariff
ATTR_TARIFF = "tariff"

# Units
UNIT_POWER = "kW"
UNIT_ENERGY = "kWh"
UNIT_VOLTAGE = "V"
UNIT_CURRENT = "A"
UNIT_APPARENT_POWER = "kVA"
UNIT_REACTIVE_POWER = "kvar"
UNIT_REACTIVE_ENERGY = "kvarh"

# Sensor types
SENSOR_TYPES = {
    # Active power
    ATTR_POWER_IN: {
        "unit": UNIT_POWER,
        "icon": "mdi:transmission-tower-import",
        "device_class": "power",
        "state_class": "measurement",
    },
    ATTR_POWER_OUT: {
        "unit": UNIT_POWER,
        "icon": "mdi:transmission-tower-export",
        "device_class": "power",
        "state_class": "measurement",
    },
    ATTR_POWER_IN_L1: {
        "unit": UNIT_POWER,
        "icon": "mdi:transmission-tower-import",
        "device_class": "power",
        "state_class": "measurement",
    },
    ATTR_POWER_IN_L2: {
        "unit": UNIT_POWER,
        "icon": "mdi:transmission-tower-import",
        "device_class": "power",
        "state_class": "measurement",
    },
    ATTR_POWER_IN_L3: {
        "unit": UNIT_POWER,
        "icon": "mdi:transmission-tower-import",
        "device_class": "power",
        "state_class": "measurement",
    },
    ATTR_POWER_OUT_L1: {
        "unit": UNIT_POWER,
        "icon": "mdi:transmission-tower-export",
        "device_class": "power",
        "state_class": "measurement",
    },
    ATTR_POWER_OUT_L2: {
        "unit": UNIT_POWER,
        "icon": "mdi:transmission-tower-export",
        "device_class": "power",
        "state_class": "measurement",
    },
    ATTR_POWER_OUT_L3: {
        "unit": UNIT_POWER,
        "icon": "mdi:transmission-tower-export",
        "device_class": "power",
        "state_class": "measurement",
    },
    # Active energy
    ATTR_ENERGY_IN: {
        "unit": UNIT_ENERGY,
        "icon": "mdi:home-import-outline",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    ATTR_ENERGY_OUT: {
        "unit": UNIT_ENERGY,
        "icon": "mdi:home-export-outline",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    ATTR_ENERGY_IN_T1: {
        "unit": UNIT_ENERGY,
        "icon": "mdi:home-import-outline",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    ATTR_ENERGY_IN_T2: {
        "unit": UNIT_ENERGY,
        "icon": "mdi:home-import-outline",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    ATTR_ENERGY_OUT_T1: {
        "unit": UNIT_ENERGY,
        "icon": "mdi:home-export-outline",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    ATTR_ENERGY_OUT_T2: {
        "unit": UNIT_ENERGY,
        "icon": "mdi:home-export-outline",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    # Voltage
    ATTR_VOLTAGE_L1: {
        "unit": UNIT_VOLTAGE,
        "icon": "mdi:sine-wave",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    ATTR_VOLTAGE_L2: {
        "unit": UNIT_VOLTAGE,
        "icon": "mdi:sine-wave",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    ATTR_VOLTAGE_L3: {
        "unit": UNIT_VOLTAGE,
        "icon": "mdi:sine-wave",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    # Current
    ATTR_CURRENT_L1: {
        "unit": UNIT_CURRENT,
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
    },
    ATTR_CURRENT_L2: {
        "unit": UNIT_CURRENT,
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
    },
    ATTR_CURRENT_L3: {
        "unit": UNIT_CURRENT,
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
    },
    # Power factor
    ATTR_POWER_FACTOR: {
        "unit": None,
        "icon": "mdi:angle-acute",
        "device_class": "power_factor",
        "state_class": "measurement",
    },
    # Apparent power
    ATTR_APPARENT_POWER: {
        "unit": UNIT_APPARENT_POWER,
        "icon": "mdi:flash-triangle",
        "state_class": "measurement",
    },
    # Reactive power
    ATTR_REACTIVE_POWER_IN: {
        "unit": UNIT_REACTIVE_POWER,
        "icon": "mdi:flash-triangle-outline",
        "state_class": "measurement",
    },
    ATTR_REACTIVE_POWER_OUT: {
        "unit": UNIT_REACTIVE_POWER,
        "icon": "mdi:flash-triangle-outline",
        "state_class": "measurement",
    },
    # Reactive energy
    ATTR_REACTIVE_ENERGY_IN: {
        "unit": UNIT_REACTIVE_ENERGY,
        "icon": "mdi:lightning-bolt-circle",
        "state_class": "total_increasing",
    },
    ATTR_REACTIVE_ENERGY_OUT: {
        "unit": UNIT_REACTIVE_ENERGY,
        "icon": "mdi:lightning-bolt-circle",
        "state_class": "total_increasing",
    },
    # Tariff
    ATTR_TARIFF: {
        "unit": None,
        "icon": "mdi:counter",
        "state_class": "measurement",
    },
}
