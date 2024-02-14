#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: $0 <ip_address_or_list_file> <firmware_file>"
    exit 1
fi

if [ ! -f "$2" ]; then
    echo "Firmware file not found: $2"
    exit 1
fi

firmware_file="$2"

if [ -f "$1" ]; then
    ip_list_file="$1"
    while IFS= read -r ip_address; do
        curl -v -F file=@$firmware_file http://$ip_address/update
        if [ $? -eq 0 ]; then
            echo "Firmware update successful for $ip_address"
        else
            echo "Firmware update failed for $ip_address"
        fi
    done < "$ip_list_file"
else
    ip_address="$1"
    curl -v -F file=@$firmware_file http://$ip_address/update
    if [ $? -eq 0 ]; then
        echo "Firmware update successful for $ip_address"
    else
        echo "Firmware update failed for $ip_address"
    fi
fi

echo "OTA updates complete."

