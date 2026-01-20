#!/usr/bin/env python3
"""
TPMS BLE monitor.
"""

# Mapping
sensors = {
    "12:30:af:00:00:83": "RR",  # Rear Right
    "12:30:af:00:01:3b": "RL",  # Rear Left
    "12:30:af:00:04:80": "FR",  # Front Right
    "12:30:af:00:03:7e": "FL",  # Front Left
}
