#!/usr/bin/env python3

import sys
import os
import requests

def main():
    if len(sys.argv) < 3:
        print("Usage: {} <ip_address_or_list_file> <firmware_file>".format(sys.argv[0]))
        sys.exit(1)

    ip_address_or_list_file = sys.argv[1]
    firmware_file = sys.argv[2]

    if not os.path.exists(firmware_file):
        print("Firmware file not found:", firmware_file)
        sys.exit(1)

    def update_firmware(ip_address):
        response = requests.post("http://{}/update".format(ip_address), files={"file": open(firmware_file, "rb")})
        if response.status_code == 200:
            print("Firmware update successful for", ip_address)
        else:
            print("Firmware update failed for", ip_address)

    if os.path.isfile(ip_address_or_list_file):
        with open(ip_address_or_list_file, "r") as f:
            for ip_address in f:
                ip_address = ip_address.strip()
                update_firmware(ip_address)
    else:
        ip_address = ip_address_or_list_file
        update_firmware(ip_address)

    print("OTA updates complete.")

if __name__ == "__main__":
    main()