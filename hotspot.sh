#!/bin/bash
case "$1" in
  start)
    nmcli device wifi hotspot ifname wlan0 ssid RPI-HOTSPOT password "motdepasse123"
    ;;
  stop)
    nmcli device disconnect wlan0
    ;;
  *)
    echo "Usage: $0 {start|stop}"
    ;;
esac
