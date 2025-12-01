#!/bin/sh

echo "Running Websockets"
python3 PiCarWebSockets.py &
sleep 10

echo "Running Godot"
./FastDrink-Godot-Headless/run.sh &


wait

echo "All files were run"


