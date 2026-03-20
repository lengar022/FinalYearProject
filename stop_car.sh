#!/bin/bash
set -e
echo "Stopping car telemetry system..."
sudo systemctl stop car-dashboard
sudo systemctl stop car-telemetry
sudo systemctl stop mosquitto
pkill -f telemetry.publisher || true
pkill -f dashboard.dashboard || true
pkill -f mosquitto_sub || true
echo "Car system stopped"