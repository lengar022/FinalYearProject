#!/bin/bash
set -e
echo "Starting car telemetry system..."
source ~/Documents/FinalYearProject/telemetrySystem/fyp_env/bin/activate
sudo systemctl start mosquitto
sudo systemctl start car-telemetry
sudo systemctl start car-dashboard
echo "Car system started"