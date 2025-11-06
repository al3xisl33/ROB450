#!/bin/bash
# zero_servo.sh
# This script zeros the Moteus servo with ID 1

# Run the moteus_tool command
moteus_tool --target 1 --zero-offset

# Optional: print a message
echo "Servo 1 zeroed."
