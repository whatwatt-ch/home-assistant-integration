"""Constants for the whatwatt integration."""

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
)

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

# Units without HA enum (no device_class available for these)
UNIT_APPARENT_POWER = "kVA"
UNIT_REACTIVE_POWER = "kvar"
UNIT_REACTIVE_ENERGY = "kvarh"

SENSOR_TYPES = {
    ATTR_POWER_IN: {
        "unit": UnitOfPower.KILO_WATT,
        "icon": "mdi:transmission-tower-import",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "precision": 2,
    },
    ATTR_POWER_OUT: {
        "unit": UnitOfPower.KILO_WATT,
        "icon": "mdi:transmission-tower-export",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "precision": 2,
    },
    ATTR_POWER_IN_L1: {
        "unit": UnitOfPower.KILO_WATT,
        "icon": "mdi:transmission-tower-import",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "precision": 2,
    },
    ATTR_POWER_IN_L2: {
        "unit": UnitOfPower.KILO_WATT,
        "icon": "mdi:transmission-tower-import",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "precision": 2,
    },
    ATTR_POWER_IN_L3: {
        "unit": UnitOfPower.KILO_WATT,
        "icon": "mdi:transmission-tower-import",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "precision": 2,
    },
    ATTR_POWER_OUT_L1: {
        "unit": UnitOfPower.KILO_WATT,
        "icon": "mdi:transmission-tower-export",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "precision": 2,
    },
    ATTR_POWER_OUT_L2: {
        "unit": UnitOfPower.KILO_WATT,
        "icon": "mdi:transmission-tower-export",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "precision": 2,
    },
    ATTR_POWER_OUT_L3: {
        "unit": UnitOfPower.KILO_WATT,
        "icon": "mdi:transmission-tower-export",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "precision": 2,
    },
    ATTR_ENERGY_IN: {
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "icon": "mdi:home-import-outline",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "precision": 1,
    },
    ATTR_ENERGY_OUT: {
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "icon": "mdi:home-export-outline",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "precision": 1,
    },
    ATTR_ENERGY_IN_T1: {
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "icon": "mdi:home-import-outline",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "precision": 1,
    },
    ATTR_ENERGY_IN_T2: {
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "icon": "mdi:home-import-outline",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "precision": 1,
    },
    ATTR_ENERGY_OUT_T1: {
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "icon": "mdi:home-export-outline",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "precision": 1,
    },
    ATTR_ENERGY_OUT_T2: {
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "icon": "mdi:home-export-outline",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "precision": 1,
    },
    ATTR_VOLTAGE_L1: {
        "unit": UnitOfElectricPotential.VOLT,
        "icon": "mdi:sine-wave",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "precision": 1,
    },
    ATTR_VOLTAGE_L2: {
        "unit": UnitOfElectricPotential.VOLT,
        "icon": "mdi:sine-wave",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "precision": 1,
    },
    ATTR_VOLTAGE_L3: {
        "unit": UnitOfElectricPotential.VOLT,
        "icon": "mdi:sine-wave",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "precision": 1,
    },
    ATTR_CURRENT_L1: {
        "unit": UnitOfElectricCurrent.AMPERE,
        "icon": "mdi:current-ac",
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "precision": 2,
    },
    ATTR_CURRENT_L2: {
        "unit": UnitOfElectricCurrent.AMPERE,
        "icon": "mdi:current-ac",
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "precision": 2,
    },
    ATTR_CURRENT_L3: {
        "unit": UnitOfElectricCurrent.AMPERE,
        "icon": "mdi:current-ac",
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "precision": 2,
    },
    ATTR_POWER_FACTOR: {
        "unit": None,
        "icon": "mdi:angle-acute",
        "device_class": SensorDeviceClass.POWER_FACTOR,
        "state_class": SensorStateClass.MEASUREMENT,
        "precision": 2,
    },
    ATTR_APPARENT_POWER: {
        "unit": UNIT_APPARENT_POWER,
        "icon": "mdi:flash-triangle",
        "state_class": SensorStateClass.MEASUREMENT,
        "precision": 2,
    },
    ATTR_REACTIVE_POWER_IN: {
        "unit": UNIT_REACTIVE_POWER,
        "icon": "mdi:flash-triangle-outline",
        "state_class": SensorStateClass.MEASUREMENT,
        "precision": 2,
    },
    ATTR_REACTIVE_POWER_OUT: {
        "unit": UNIT_REACTIVE_POWER,
        "icon": "mdi:flash-triangle-outline",
        "state_class": SensorStateClass.MEASUREMENT,
        "precision": 2,
    },
    ATTR_REACTIVE_ENERGY_IN: {
        "unit": UNIT_REACTIVE_ENERGY,
        "icon": "mdi:lightning-bolt-circle",
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "precision": 1,
    },
    ATTR_REACTIVE_ENERGY_OUT: {
        "unit": UNIT_REACTIVE_ENERGY,
        "icon": "mdi:lightning-bolt-circle",
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "precision": 1,
    },
    ATTR_TARIFF: {
        "unit": None,
        "icon": "mdi:counter",
        "precision": 0,
    },
}
