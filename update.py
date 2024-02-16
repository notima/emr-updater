#!/usr/bin/env python3

import sys
import os
import requests
from time import sleep

def main():
    if len(sys.argv) < 3:
        print("Usage: {} <ip_address_or_list_file> <firmware_file>".format(sys.argv[0]))
        sys.exit(1)

    ip_address_or_list_file = sys.argv[1]
    firmware_file = sys.argv[2]

    if not os.path.exists(firmware_file):
        print("Firmware file not found:", firmware_file)
        sys.exit(1)

    def change_protocol(ip_address, protocol):
        payload = {"config": {"meter": {"protocol": protocol}}}

        change_protocol_response = requests.post("http://" + ip_address + "/rpc/Config.set", json = payload)
        
        if change_protocol_response.status_code != 200:
            raise Exception("Could not change protocol for", ip_address, ". Status: " + str(change_protocol_response.status_code))
        save_protocol = requests.post("http://" + ip_address + "/rpc/Config.save")
        
        if change_protocol_response.status_code != 200:
            raise Exception("Could not save config for", ip_address)
            
        reboot_response_1 = requests.get("http://" + ip_address + "/rpc/sys.reboot")
        
        if reboot_response_1.status_code != 200:
            raise Exception("Could not reboot", ip_address, ". status:", reboot_response_1.status_code)
        else:
            sleep(5)

    def update_firmware(ip_address):
        try:
            change_protocol(ip_address, 201)
        except Exception as error:
            print("failed to change protocol", error)
            return
            
        response = requests.post("http://{}/update".format(ip_address), files={"file": open(firmware_file, "rb")})
        
        if response.status_code == 200:
            try:
                change_protocol(ip_address, 0)
                print("Firmware update successful for", ip_address)
            except Exception as error:
                print("failed to restore protocol", error)
        else:
            print("Firmware update failed for", ip_address)
            return
        

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
