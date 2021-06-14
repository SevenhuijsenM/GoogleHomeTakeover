import os
from scapy.all import *
from threading import Thread
import threading
import pandas
import time
import asyncio

def add_wlan_names(dropdown_menu): 
    # Retrieve interfaces to use for monitoring the internet traffic
    print("Getting the wifi devices")
    
    # Read from the wireless connection file in linux
    f = open("/proc/net/dev")

    # Get the wireless file, with the first two columns dropped (gives column info)
    wlanConnectors = f.read().splitlines()[2:]
    
    # close the file after reading the wireless connection
    f.close()

    # filter the wireless connections to the device names
    wlanNames = [connection.split()[0][0:-1] for connection in wlanConnectors]

    wlanNames = ["1", "2"];

    for wlan in wlanNames:
        dropdown_menu.addItem(wlan)

def set_monitor_mode(network_interface):
    print("Setting op monitor mode for " + network_interface)
    os.system("sudo systemctl stop NetworkManager")
    os.system("sudo ifconfig " + network_interface + " down")
    os.system("sudo airmon-ng kill")
    os.system("sudo iwconfig " + network_interface + " mode monitor")    
    os.system("sudo ifconfig " + network_interface + " up")
    os.system("sudo airmon-ng start " + network_interface)
    print("Done setting up monitor mode for " + network_interface)

def get_networks(network_monitor, networks, stop_event):    
    
    def process_packet(packet):
        if packet.haslayer("Dot11Beacon"):
            # Get the mac address
            bssid = packet["Dot11"].addr2
            if bssid not in networks.index.values:
                # Get the name of the network
                ssid = packet["Dot11Elt"].info.decode()

                # Try to get the signal strength
                try: 
                    dbm_signal = packet.dBm_AntSignal
                except:
                    dbm_signal = "N/A"
                
                # Get the network stats
                stats = packet["Dot11Beacon"].network_stats()

                # Get the channel of the AP
                channel = stats.get("channel")

                # Get the cryptographic encryption
                crypto = stats.get("crypto")
                networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)

    def change_channel(stop_event):
        ch = 1
        while not stop_event.is_set():
            # Keep changing the channel from 1 to 14
            # os.system(f"iwconfig {network_monitor} channel {ch}")
            ch = ch % 14 + 1
            time.sleep(0.5)

    # Start changing channels
    channel_changer = Thread(target=change_channel, args=(stop_event,))
    channel_changer.daemon = True
    channel_changer.start()
    
    sniff(prn=process_packet, iface=network_monitor, stop_filter=lambda p: stop_event.is_set())
    networks.loc["1"] = ("1", "1", "1", "1")

def get_devices(network_monitor, wifi_network, devices, stop_event):    
    devices.loc["1"] = ("1")

def block_device(network_monitor, wifi_network, device, stop_event):
    print(network_monitor)