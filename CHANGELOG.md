# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.4.0] - 2025-04-30

### Added
- Extended sensor support: current (L1/L2/L3), power factor, apparent power, reactive power/energy, tariff
- Translations for German, French, Italian, and Polish
- Reconfigure flow for updating device settings
- Diagnostics support
- E2E test suite with Docker Compose

### Fixed
- MQTT API compatibility and callback handling
- Device info initialization
- Optional IP address handling
- Tariff value parsing
- Unit assignments for all sensor types

## [0.3.0] - 2025-03-27

### Added
- Initial public release
- Power consumption and generation monitoring (total and per-phase)
- Energy usage tracking (total and per-tariff)
- Voltage monitoring for all three phases
- HACS compatibility
- MQTT-based communication with whatwatt Go devices
- Configuration flow with MQTT topic and device IP
- Configuration button for device web interface access
