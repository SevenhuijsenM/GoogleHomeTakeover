from re import L
import asyncio
from network import get_networks, get_wlan_names, set_monitor_mode
import tkinter as tk
import time
from threading import Thread
import pandas


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        # Create the widgets
        self.create_widgets()

        self.master.minsize(200, 200)

    def create_dropdown(self):
        # Fetch all network devices
        wlanDevices = get_wlan_names()

        # Create a variable that can be set in a dropdown
        self.wlanVariable = tk.StringVar(self)

        # Set the default value to the first in the list
        self.wlanVariable.set(wlanDevices[0])

        # Create the dropdowns
        dropdown = tk.OptionMenu(self, self.wlanVariable, *wlanDevices)
        dropdown.pack()

        
    def create_Monitor_button(self):
        self.monitor_button = tk.Button(self)
        self.monitor_button["text"] = "Scan selected network device"
        self.monitor_button["command"] = self.monitor_network
        self.monitor_button.pack(side="top")

    def create_input_field(self):
        timerLabel = tk.Label(self, text="Timer counter")
        timerLabel.pack(side="top")
        self.entry_box_timer = tk.Entry(self)
        self.entry_box_timer["text"] = "60"
        self.entry_box_timer.pack(side="top")
        
    def create_widgets(self):
        # Create a dropdown with available wlan devices
        self.create_dropdown()

        # Create a label for the timer
        self.create_input_field()

        # Create a button to monitor the selected networm
        self.create_Monitor_button()
        
    def monitor_network(self):
        # Set the network adapter to monitor mode
        set_monitor_mode(self.wlanVariable.get())

        # Create a dataframe that will contain all nearby data points
        networks = pandas.DataFrame(columns=["BSSID", "SSID", " dBm_Signal", "Channel", "Crypto"])

        # Set the index to BSSID ( mac address )
        networks.set_index("BSSID", inplace=True)

        # Create an async task for this to maintain a responsive gui
        Thread(target=get_networks, args=(self.wlanVariable.get(), int(self.entry_box_timer.get()), networks, )).start()

        # Create a dropdown menu for the names
        network_options = networks['SSID']
                # Create a variable that can be set in a dropdown
        self.network_variable = tk.StringVar(self)

        # Create the dropdowns
        dropdown = tk.OptionMenu(self, self.wlanVariable, *network_options)
        dropdown.pack()

root = tk.Tk()
app = Application(master=root)
app.mainloop()