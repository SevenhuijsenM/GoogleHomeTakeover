# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from network import *
from threading import Thread, Timer
import threading
import pandas

class ui_main_window(object):
    def setup_ui(self, main_window):

        # The boolean for scanning for networks
        self.scanning_wifi = False
        self.scanning_devices = False
        self.blocking_device = False

        # Create a font size for all the headers
        font = QtGui.QFont()
        font.setPointSize(16)

        # Create the main window with a vertical layout
        main_window.setObjectName("main_window")
        main_window.resize(828, 195)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.vertical_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.vertical_layout.setObjectName("vertical_layout")

        # Create a tab widget
        self.tab_widget = QtWidgets.QTabWidget(self.central_widget)
        self.tab_widget.setObjectName("tab_widget")

        # Create a tab for the network interface
        self.network_interface_tab = QtWidgets.QWidget()
        self.network_interface_tab.setObjectName("network_interface_tab")
        self.step1_label = QtWidgets.QLabel(self.network_interface_tab)
        self.step1_label.setGeometry(QtCore.QRect(0, 0, 781, 31))
        self.step1_label.setMaximumSize(QtCore.QSize(801, 16777215))
        self.step1_label.setFont(font)
        self.step1_label.setAlignment(QtCore.Qt.AlignCenter)
        self.step1_label.setObjectName("step1_label")
        self.input_box_interfaces = QtWidgets.QComboBox(self.network_interface_tab)
        self.input_box_interfaces.setGeometry(QtCore.QRect(190, 40, 411, 22))
        self.input_box_interfaces.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.input_box_interfaces.setInsertPolicy(QtWidgets.QComboBox.InsertAtCurrent)
        self.input_box_interfaces.setMinimumContentsLength(0)
        self.input_box_interfaces.setObjectName("input_box_interfaces")
        self.tab_widget.addTab(self.network_interface_tab, "")

        # Create a tab for scanning WiFi Networks
        self.scan_wifi_tab = QtWidgets.QWidget()
        self.scan_wifi_tab.setObjectName("scan_wifi_tab")
        self.step2_label = QtWidgets.QLabel(self.scan_wifi_tab)
        self.step2_label.setGeometry(QtCore.QRect(0, 0, 781, 31))
        self.step2_label.setFont(font)
        self.step2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.step2_label.setObjectName("step2_label")
        self.scan_duration_spin_box = QtWidgets.QSpinBox(self.scan_wifi_tab)
        self.scan_duration_spin_box.setGeometry(QtCore.QRect(240, 50, 301, 31))
        self.scan_duration_spin_box.setObjectName("scan_duration_spin_box")
        self.scan_duration_spin_box.setRange(0, 1000)
        self.scan_duration_spin_box.setValue(20)
        self.scan_wifi_button = QtWidgets.QPushButton(self.scan_wifi_tab)
        self.scan_wifi_button.setGeometry(QtCore.QRect(240, 90, 311, 31))
        self.scan_wifi_button.setObjectName("scan_wifi_button")
        self.scan_wifi_button.clicked.connect(self.on_click_scan_wifi)
        self.scan_duration_seconds = QtWidgets.QLabel(self.scan_wifi_tab)
        self.scan_duration_seconds.setGeometry(QtCore.QRect(0, 29, 781, 21))
        self.scan_duration_seconds.setAlignment(QtCore.Qt.AlignCenter)
        self.scan_duration_seconds.setObjectName("scan_duration_seconds")
        self.tab_widget.addTab(self.scan_wifi_tab, "")

        # Create a tab for scanning for devices
        self.select_wifi_tab = QtWidgets.QWidget()
        self.select_wifi_tab.setObjectName("select_wifi_tab")
        self.step3_label = QtWidgets.QLabel(self.select_wifi_tab)
        self.step3_label.setGeometry(QtCore.QRect(0, 0, 781, 31))
        self.step3_label.setFont(font)
        self.step3_label.setAlignment(QtCore.Qt.AlignCenter)
        self.step3_label.setObjectName("step3_label")
        self.wifi_scan_combo_box = QtWidgets.QComboBox(self.select_wifi_tab)
        self.wifi_scan_combo_box.setGeometry(QtCore.QRect(200, 31, 371, 21))
        self.wifi_scan_combo_box.setObjectName("wifi_scan_combo_box")
        self.scan_duration_devices_label = QtWidgets.QLabel(self.select_wifi_tab)
        self.scan_duration_devices_label.setGeometry(QtCore.QRect(310, 50, 781, 16))
        self.scan_duration_devices_label.setObjectName("scan_duration_devices_label")
        self.scan_duration_devices_spin_box = QtWidgets.QSpinBox(self.select_wifi_tab)
        self.scan_duration_devices_spin_box.setGeometry(QtCore.QRect(240, 65, 301, 31))
        self.scan_duration_devices_spin_box.setObjectName("scan_duration_devices_spin_box")
        self.scan_duration_devices_spin_box.setRange(0, 100)
        self.scan_duration_devices_spin_box.setValue(5)
        self.scan_devices_button = QtWidgets.QPushButton(self.select_wifi_tab)
        self.scan_devices_button.setGeometry(QtCore.QRect(200, 100, 371, 31))
        self.scan_devices_button.setObjectName("scan_devices_button")
        self.scan_devices_button.clicked.connect(self.on_click_scan_devices)
        self.tab_widget.addTab(self.select_wifi_tab, "")

        # Create a tab for selecting and blocking a network
        self.block_device_tab = QtWidgets.QWidget()
        self.block_device_tab.setObjectName("block_device_tab")
        self.step4_label = QtWidgets.QLabel(self.block_device_tab)
        self.step4_label.setGeometry(QtCore.QRect(0, 0, 781, 31))
        self.step4_label.setFont(font)
        self.step4_label.setAlignment(QtCore.Qt.AlignCenter)
        self.step4_label.setObjectName("step4_label")
        self.device_block_combo_box = QtWidgets.QComboBox(self.block_device_tab)
        self.device_block_combo_box.setGeometry(QtCore.QRect(200, 50, 371, 21))
        self.device_block_combo_box.setObjectName("device_block_combo_box")
        self.block_device_label = QtWidgets.QLabel(self.block_device_tab)
        self.block_device_label.setGeometry(QtCore.QRect(300, 30, 311, 16))
        self.block_device_label.setObjectName("Scan_Duration_Label")
        self.block_device_button = QtWidgets.QPushButton(self.block_device_tab)
        self.block_device_button.setGeometry(QtCore.QRect(200, 80, 371, 31))
        self.block_device_button.setObjectName("block_device_button")
        self.block_device_button.clicked.connect(self.on_click_block_device)
        self.tab_widget.addTab(self.block_device_tab, "")

        # Create a tab for taking over the google home
        self.take_over_google_tab = QtWidgets.QWidget()
        self.take_over_google_tab.setObjectName("take_over_google_tab")
        self.step5_label = QtWidgets.QLabel(self.take_over_google_tab)
        self.step5_label.setGeometry(QtCore.QRect(0, 0, 781, 31))
        self.step5_label.setFont(font)
        self.step5_label.setAlignment(QtCore.Qt.AlignCenter)
        self.step5_label.setObjectName("step5_label")
        self.tab_widget.addTab(self.take_over_google_tab, "")

        # Set up the layout and the main frame properly
        self.vertical_layout.addWidget(self.tab_widget)
        main_window.setCentralWidget(self.central_widget)

        # Rename some of the components
        self.retranslate_ui(main_window)

        # Set up the pages
        self.set_up_pages()
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def set_up_pages(self):
        # Add the interfaces to the dropdown
        add_wlan_names(self.input_box_interfaces)

        # Create a dataframe that will contain all nearby networks
        self.networks = pandas.DataFrame(columns=["BSSID", "SSID", " dBm_Signal", "Channel", "Crypto"])

        # Set the index to BSSID ( mac address )
        self.networks.set_index("BSSID", inplace=True)

        # Create a dataframe that will contain all nearby devices on the network
        self.devices = pandas.DataFrame(columns=["MAC", "Device_Type"])

        # Set the index to BSSID ( mac address )
        self.devices.set_index("MAC", inplace=True)

        # Set the loaded page to the 0th pages, the first step
        self.tab_widget.setCurrentIndex(0)

        # Disable all other pages
        self.disable_tabs(0)

        if self.input_box_interfaces.count() > 0:
            self.tab_widget.setTabEnabled(1, True)


    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Google Home Takeover"))
        self.step1_label.setText(_translate("main_window", "Select Networking Interface"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.network_interface_tab), _translate("main_window", "Step 1"))
        self.step2_label.setText(_translate("main_window", "Scan for Wi-Fi Networks"))
        self.scan_wifi_button.setText(_translate("main_window", "Start scanning"))
        self.scan_duration_seconds.setText(_translate("main_window", "Scanning duration in seconds ( Recommended > 15 )"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.scan_wifi_tab), _translate("main_window", "Step 2"))
        self.step3_label.setText(_translate("main_window", "Select the Wi-Fi network that contains a Google Home"))
        self.scan_duration_devices_label.setText(_translate("main_window", "Scanning duration in seconds"))
        self.block_device_label.setText(_translate("main_window", "Select the device that will be Blocked"))
        self.scan_devices_button.setText(_translate("main_window", "Start Scanning"))
        self.block_device_button.setText(_translate("main_window", "Start Blocking"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.select_wifi_tab), _translate("main_window", "Step 3"))
        self.step4_label.setText(_translate("main_window", "Block the google home"))
        self.step5_label.setText(_translate("main_window", "Take over the Google Home on your Phone"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.block_device_tab), _translate("main_window", "Step 4"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.take_over_google_tab), _translate("main_window", "Step 5"))

    def enable_tabs(self, index):
        # This function enables all tabs up to i
        for i in range(index):
            self.tab_widget.setTabEnabled(i, True)

    def disable_tabs(self, index):
        # This function disables all tabs except for the index i 
        AMOUNT_TABS = 5 # Define the total amount of tabs

        self.tab_widget.setTabEnabled(index, True)

        for i in range(AMOUNT_TABS):
            if not i == index:
                self.tab_widget.setTabEnabled(i, False)

    def on_click_scan_wifi(self):
        self.scanning_wifi = not self.scanning_wifi

        # The program is searching for networks
        if self.scanning_wifi:
            # Set the network adapter to monitor mode
            set_monitor_mode(self.input_box_interfaces.currentText())

            # Clear all the  previously scanned networks fro mthe combobox
            self.wifi_scan_combo_box.clear()

            # A stop event in order to stop the threat
            self.stop_event = threading.Event()

            # Create a timer that waits for the x amount of seconds
            self.scan_wifi_timer = Timer(self.scan_duration_spin_box.value(), self.stop_event_wifi)
            self.scan_wifi_timer.start()

            # Create an async task for this to maintain a responsive gui
            Thread(target=get_networks, args=(self.input_box_interfaces.currentText(), self.networks, self.stop_event)).start()

            self.scan_wifi_button.setText("Stop scanning")
            
            # Disable all tabs except for the running one
            self.disable_tabs(1)

        else:
            self.stop_event_wifi()

    def stop_event_wifi(self):
        if not self.stop_event.isSet():
            # Cancel the timer if this is ran by the timer
            if self.scan_wifi_timer.is_alive():
                self.scan_wifi_timer.cancel()

            self.stop_event.set()
            self.scan_wifi_button.setText("Start scanning")
            
            # Enable the previous tabs + the next one if a network is found
            self.enable_tabs(1)
            if len(self.networks) > 0:
                self.tab_widget.setTabEnabled(2, True)

            # Put all the scanned networks in the combobox on step 3
            for i in range(len(self.networks)):
                self.wifi_scan_combo_box.addItem(self.networks.iloc[i]["SSID"])

    def on_click_scan_devices(self):
        self.scanning_devices = not self.scanning_devices

        # The program is searching for devices on the network
        if self.scanning_devices:
            # Clear all the  previously scanned networks fro mthe combobox
            self.device_block_combo_box.clear()

            # A stop event in order to stop the threat
            self.stop_event = threading.Event()

            # Create a timer that waits for the x amount of seconds
            self.scan_device_timer = Timer(self.scan_duration_devices_spin_box.value(), self.stop_event)
            self.scan_device_timer.start()

            # Create an async task for this to maintain a responsive gui
            Thread(target=get_devices, args=(self.input_box_interfaces.currentText(), self.wifi_scan_combo_box.currentText(), self.devices, self.stop_event)).start()

            self.scan_devices_button.setText("Stop scanning")
            self.disable_tabs(2)

        else:
            self.stop_event_devices()

    def stop_event_devices(self):
        if not self.stop_event.isSet():
            # Cancel the timer if this is ran by the timer
            if self.scan_device_timer.is_alive():
                self.scan_device_timer.cancel()

            self.stop_event.set()
            self.scan_devices_button.setText("Start scanning")
            
            # Enable the previous tabs + the next one if a device is found
            self.enable_tabs(2)
            if len(self.devices) > 0:
                self.tab_widget.setTabEnabled(3, True)

            # Put all the scanned devices in the combobox on step 4
            for i in range(len(self.devices)):
                self.device_block_combo_box.addItem(self.devices.iloc[i]['Device_Type'])
            
    def on_click_block_device(self):
        self.blocking_device = not self.blocking_device

        # The program is searching for devices on the network
        if self.blocking_device:
            # A stop event in order to stop the threat
            self.stop_event = threading.Event()

            # Create an async task for this to maintain a responsive gui
            Thread(target=block_device, args=(self.input_box_interfaces.currentText(), self.wifi_scan_combo_box.currentText(), self.device_block_combo_box.currentText(), self.stop_event)).start()

            self.block_device_button.setText("Stop blocking")
            self.disable_tabs(3)
            self.tab_widget.setTabEnabled(4, True)

        else:
            if not self.stop_event.isSet():
                self.stop_event.set()
                self.block_device_button.setText("Start blocking")
                self.enable_tabs(3)
                self.tab_widget.setTabEnabled(4, False)
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = ui_main_window()
    ui.setup_ui(main_window)
    main_window.show()
    sys.exit(app.exec_())

