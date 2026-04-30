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
  "energy_in":"${1_8_0}",
  "energy_out":"${2_8_0}",
  "voltage_l1":"${32_7_0}",
  "voltage_l2":"${52_7_0}",
  "voltage_l3":"${72_7_0}"
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

- **Power In**: Current power being drawn from the grid (W)
- **Power Out**: Current power being exported to the grid (W)
- **Energy In**: Total energy consumed from the grid (kWh)
- **Energy Out**: Total energy exported to the grid (kWh)
- **Voltage L1**: Voltage level on phase L1 (V)
- **Voltage L2**: Voltage level on phase L2 (V)
- **Voltage L3**: Voltage level on phase L3 (V)

### Buttons

- **Configuration**: Opens the device's configuration page in your web browser

## MQTT Payload Format

The whatwatt Go device sends data in the following JSON format:

```json
{
  "sys_id": "device-id",
  "meter_id": "meter-id",
  "time": "timestamp",
  "power_in": 1234.5,
  "power_out": 0.0,
  "energy_in": 12345.6,
  "energy_out": 123.4,
  "voltage_l1": 230.1,
  "voltage_l2": 231.2,
  "voltage_l3": 229.8
}
```

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
