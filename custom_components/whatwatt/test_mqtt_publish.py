#!/usr/bin/env python3
"""
Test script for whatwatt Home Assistant integration.
This script publishes a sample MQTT message to test the integration.

Usage:
  python3 test_mqtt_publish.py --broker localhost --port 1883 --topic whatwatt/test --interval 10

Requirements:
  pip install paho-mqtt
"""

import argparse
import json
import time
from datetime import datetime
import random
import paho.mqtt.client as mqtt

# Default values
DEFAULT_BROKER = "localhost"
DEFAULT_PORT = 1883
DEFAULT_TOPIC = "whatwatt/test"
DEFAULT_INTERVAL = 10  # seconds
DEFAULT_SYS_ID = "whatwatt-test"
DEFAULT_METER_ID = "meter-test"

def generate_message():
    """Generate a sample whatwatt message with some random variations."""
    power_in = random.uniform(800, 2500)
    power_out = random.uniform(0, 100) if random.random() > 0.7 else 0
    
    # Accumulate energy over time
    global energy_in, energy_out
    energy_in += power_in / 3600  # Convert W to Wh and then to kWh
    energy_out += power_out / 3600
    
    # Generate realistic voltage values
    voltage_l1 = random.uniform(220, 240)
    voltage_l2 = random.uniform(220, 240)
    voltage_l3 = random.uniform(220, 240)
    
    return {
        "sys_id": DEFAULT_SYS_ID,
        "meter_id": DEFAULT_METER_ID,
        "time": datetime.utcnow().isoformat() + "Z",
        "power_in": round(power_in, 1),
        "power_out": round(power_out, 1),
        "energy_in": round(energy_in / 1000, 3),  # Convert Wh to kWh
        "energy_out": round(energy_out / 1000, 3),
        "voltage_l1": round(voltage_l1, 1),
        "voltage_l2": round(voltage_l2, 1),
        "voltage_l3": round(voltage_l3, 1)
    }

def on_connect(client, userdata, flags, rc):
    """Callback for when the client connects to the broker."""
    if rc == 0:
        print(f"Connected to MQTT broker at {args.broker}:{args.port}")
    else:
        print(f"Failed to connect to MQTT broker, return code: {rc}")

def main(args):
    """Main function to publish MQTT messages."""
    client = mqtt.Client()
    client.on_connect = on_connect
    
    # Connect to the broker
    try:
        client.connect(args.broker, args.port, 60)
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        return
    
    # Start the MQTT loop in a background thread
    client.loop_start()
    
    try:
        print(f"Publishing messages to topic '{args.topic}' every {args.interval} seconds. Press Ctrl+C to stop.")
        while True:
            message = generate_message()
            payload = json.dumps(message)
            print(f"Publishing: {payload}")
            client.publish(args.topic, payload)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    # Initialize energy counters
    energy_in = 0
    energy_out = 0
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Test MQTT publisher for whatwatt integration")
    parser.add_argument("--broker", default=DEFAULT_BROKER, help=f"MQTT broker address (default: {DEFAULT_BROKER})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"MQTT broker port (default: {DEFAULT_PORT})")
    parser.add_argument("--topic", default=DEFAULT_TOPIC, help=f"MQTT topic to publish to (default: {DEFAULT_TOPIC})")
    parser.add_argument("--interval", type=int, default=DEFAULT_INTERVAL, help=f"Publish interval in seconds (default: {DEFAULT_INTERVAL})")
    args = parser.parse_args()
    
    main(args)
