# whatwatt Home Assistant Integration

Custom Home Assistant integration for whatwatt Go devices that read data from electricity meters.

## Overview

This integration allows Home Assistant to receive and display data from whatwatt Go devices via MQTT. It provides sensors for power consumption, power generation, energy usage, and voltage levels for all three phases.

![whatwatt Logo](https://avatars.githubusercontent.com/u/201613898?s=200&v=4)

## Requirements

- **MQTT Integration**: This integration requires the MQTT integration to be set up in Home Assistant. If you don't have MQTT configured:
  1. Go to Settings > Devices & Services > Add Integration
  2. Search for "MQTT" and follow the setup instructions
  3. If you're using Home Assistant OS, we recommend using the Mosquitto MQTT Broker add-on

- **whatwatt Go Device**: Your device must be configured to publish data to your MQTT broker

## Features

- Easy setup through the Home Assistant UI
- Real-time monitoring of electricity usage
- Support for multiple whatwatt devices
- Access to device configuration page

## Installation

### Option 1: HACS (Home Assistant Community Store)

1. Open HACS in your Home Assistant instance
2. Go to "Integrations"
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add the URL `https://github.com/whatwatt-ch/home-assistant-integration` with category "Integration"
5. Click "Add"
6. Search for "whatwatt" in the integrations tab
7. Click "Download"
8. Restart Home Assistant

### Option 2: Manual Installation Script

1. Clone this repository:
   ```bash
   git clone https://github.com/whatwatt-ch/home-assistant-integration.git
   cd home-assistant-integration
   ```

2. Run the installation script:
   ```bash
   ./install.sh
   ```
   
   By default, the script will install the integration to `~/.homeassistant/custom_components/`. If your Home Assistant configuration directory is different, use the `-d` option:
   ```bash
   ./install.sh -d /path/to/your/config
   ```

3. Restart Home Assistant

### Option 3: Manual Installation

1. Copy the `custom_components/whatwatt` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

### whatwatt Go Setup

Before using this integration, you need to configure your whatwatt Go device to send data to your MQTT broker. See the [detailed configuration guide](custom_components/whatwatt/README.md#whatwatt-go-configuration) for step-by-step instructions.

### Home Assistant Setup

1. Make sure your whatwatt Go device is configured to send data to your MQTT broker
2. In Home Assistant, go to Settings > Devices & Services
3. Click "Add Integration" and search for "whatwatt"
4. Enter the MQTT topic that your whatwatt Go device is publishing to
5. Enter the IP address of your whatwatt Go device (for accessing the configuration page)
6. Optionally, provide a custom name for the device

## Testing

A test script is included to simulate a whatwatt device sending MQTT messages:

```bash
cd custom_components/whatwatt
pip install paho-mqtt
./test_mqtt_publish.py --broker localhost --port 1883 --topic whatwatt/test --interval 10
```

## Documentation

For detailed documentation, see the [README.md](custom_components/whatwatt/README.md) file in the `custom_components/whatwatt` directory.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

Thanks to [@Bugga-CH](https://github.com/Bugga-CH) for identifying and reporting critical bugs in the original integration through their [community fork](https://github.com/Bugga-CH/home-assistant-integration-fix). Their contributions helped improve MQTT compatibility, device initialization, and overall stability of this integration.

## Support

For issues, feature requests, or questions, please open an issue on the [GitHub repository](https://github.com/whatwatt-ch/home-assistant-integration/issues).
