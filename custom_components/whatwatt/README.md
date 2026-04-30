# whatwatt Home Assistant Integration

Custom Home Assistant integration for whatwatt Go devices that read data from electricity meters.

![whatwatt Logo](https://avatars.githubusercontent.com/u/201613898?s=200&v=4)

## Requirements

- **MQTT Integration**: This integration requires the MQTT integration to be set up in Home Assistant. If you don't have MQTT configured:
  1. Go to Settings > Devices & Services > Add Integration
  2. Search for "MQTT" and follow the setup instructions
  3. If you're using Home Assistant OS, we recommend using the Mosquitto MQTT Broker add-on

- **whatwatt Go Device**: Your device must be configured to publish data to your MQTT broker

## Features

- Connects to whatwatt Go devices via MQTT
- Displays real-time power consumption and generation data
- Shows voltage levels for all three phases
- Tracks total energy consumption and generation
- Provides easy access to the device's configuration page

## whatwatt Go Configuration

Before setting up the integration in Home Assistant, you need to configure your whatwatt Go device to send data to your MQTT broker:

### Step 1: Access WebUI of whatwatt Go

Open your browser and enter the IP address of the whatwatt GO device (e.g., http://192.168.1.100) into the address field.

### Step 2: Configure MQTT Settings

1. Navigate to MQTT Settings in the WebUI
2. Enter the following details and activate MQTT:
   - **Broker URL**: mqtt://<broker_address> (e.g., mqtt://192.168.1.101)
   - **Username and Password**: Provide your MQTT broker credentials
   - **Client ID**: whatwattGO (or any other unique identifier)
   - **Topic**: energy/whatwatt/go (or any other topic structure)
   - **Template**: Use the following JSON template (add/remove OBIS codes according to your needs):
   
```json
{
  "sys_id":"${sys.id}",
  "meter_id":"${meter.id}",
  "time":"${timestamp}",
  "power_in":"${1_7_0}",
  "power_out":"${2_7_0}",
  "power_in_l1":"${21_7_0}",
  "power_in_l2":"${41_7_0}",
  "power_in_l3":"${61_7_0}",
  "power_out_l1":"${22_7_0}",
  "power_out_l2":"${42_7_0}",
  "power_out_l3":"${62_7_0}",
  "energy_in":"${1_8_0}",
  "energy_out":"${2_8_0}",
  "energy_in_t1":"${1_8_1}",
  "energy_in_t2":"${1_8_2}",
  "energy_out_t1":"${2_8_1}",
  "energy_out_t2":"${2_8_2}",
  "voltage_l1":"${32_7_0}",
  "voltage_l2":"${52_7_0}",
  "voltage_l3":"${72_7_0}",
  "current_l1":"${31_7_0}",
  "current_l2":"${51_7_0}",
  "current_l3":"${71_7_0}",
  "power_factor":"${13_7_0}",
  "apparent_power":"${9_7_0}",
  "reactive_power_in":"${3_7_0}",
  "reactive_power_out":"${4_7_0}",
  "reactive_energy_in":"${3_8_0}",
  "reactive_energy_out":"${4_8_0}",
  "tariff":"${tariff}"
}
```

> Note: OBIS values delivered by your meter can be identified in WebUI > Live

### Step 3: Set Reporting Period

Navigate to WebUI > System and set the "Interval to Systems" to 30 seconds.

## Installation

### HACS (Home Assistant Community Store)

1. Open HACS in your Home Assistant instance
2. Go to "Integrations"
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add the URL `https://github.com/whatwatt-ch/home-assistant-integration` with category "Integration"
5. Click "Add"
6. Search for "whatwatt" in the integrations tab
7. Click "Download"
8. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [GitHub repository](https://github.com/whatwatt-ch/home-assistant-integration)
2. Extract the `custom_components/whatwatt` folder to your Home Assistant's `custom_components` directory
3. Restart Home Assistant

## Home Assistant Configuration

1. In Home Assistant, go to Settings > Devices & Services
2. Click "Add Integration" and search for "whatwatt"
3. Enter the MQTT topic that your whatwatt Go device is publishing to (the same topic you configured in the whatwatt Go device)
4. Enter the IP address of your whatwatt Go device (for accessing the configuration page)
5. Optionally, provide a custom name for the device

## Available Entities

For each whatwatt Go device, the following entities will be created:

### Sensors

| Sensor | Unit | OBIS | Description |
|--------|------|------|-------------|
| Power In | kW | 1.7.0 | Active power import total |
| Power Out | kW | 2.7.0 | Active power export total |
| Power In L1/L2/L3 | kW | 21/41/61.7.0 | Active power import per phase |
| Power Out L1/L2/L3 | kW | 22/42/62.7.0 | Active power export per phase |
| Energy In | kWh | 1.8.0 | Active energy import total |
| Energy Out | kWh | 2.8.0 | Active energy export total |
| Energy In T1/T2 | kWh | 1.8.1/2 | Active energy import per tariff |
| Energy Out T1/T2 | kWh | 2.8.1/2 | Active energy export per tariff |
| Voltage L1/L2/L3 | V | 32/52/72.7.0 | Voltage per phase |
| Current L1/L2/L3 | A | 31/51/71.7.0 | Current per phase |
| Power Factor | — | 13.7.0 | Power factor (0–1) |
| Apparent Power | kVA | 9.7.0 | Apparent power total |
| Reactive Power In | kvar | 3.7.0 | Reactive power import |
| Reactive Power Out | kvar | 4.7.0 | Reactive power export |
| Reactive Energy In | kvarh | 3.8.0 | Reactive energy import |
| Reactive Energy Out | kvarh | 4.8.0 | Reactive energy export |
| Tariff | — | 96.14.0 | Active tariff (1–4) |

> Only sensors present in your MQTT template will appear in Home Assistant. Add/remove fields from your whatwatt go template as needed.

### Buttons

- **Configuration**: Logs the device configuration URL

## MQTT Payload Format

The whatwatt Go device sends data in the following JSON format:

```json
{
  "sys_id": "whatwatt-123456",
  "meter_id": "meter-789012",
  "time": "2025-03-27T22:00:00Z",
  "power_in": 1.23,
  "power_out": 0.0,
  "power_in_l1": 0.45,
  "power_in_l2": 0.38,
  "power_in_l3": 0.40,
  "energy_in": 12345.6,
  "energy_out": 123.4,
  "voltage_l1": 230.1,
  "voltage_l2": 231.2,
  "voltage_l3": 229.8,
  "current_l1": 1.96,
  "current_l2": 1.65,
  "current_l3": 1.74,
  "power_factor": 0.98,
  "apparent_power": 1.26,
  "reactive_power_in": 0.25,
  "reactive_power_out": 0.0,
  "tariff": 1
}
```

> Fields present in the payload depend on your MQTT template configuration on the whatwatt go device. Only included fields will create sensor entities.

## Troubleshooting

### MQTT Connection Issues

- Ensure that the MQTT integration is properly set up in Home Assistant
- Verify that the whatwatt Go device is correctly configured to publish to the MQTT broker
- Check that the MQTT topic in the integration configuration matches the one configured on the device

### Missing Sensors

- The sensors will appear only after the first MQTT message is received
- Check the Home Assistant logs for any errors related to the whatwatt integration

### Configuration Button Not Working

- The configuration button opens the device's web interface in your browser
- Ensure that the IP address entered during setup is correct and accessible from your network
- The button may not work if Home Assistant is running in a container or on a system without a GUI

## Support

For issues, feature requests, or questions, please open an issue on the [GitHub repository](https://github.com/whatwatt-ch/home-assistant-integration/issues).
