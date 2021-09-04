# SPDX-FileCopyrightText: Copyright (c) 2019 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_esp32spi_wifimanager`
================================================================================

WiFi Manager for making ESP32 SPI as WiFi much easier

* Author(s): Melissa LeBlanc-Williams, ladyada
"""

# pylint: disable=no-name-in-module

from time import sleep
from micropython import const
from driver.esp32spi import esp32spi


# pylint: disable=too-many-instance-attributes
class ESPSPI_WiFiManager:
    """
    A class to help manage the Wifi connection
    """

    NORMAL = const(1)
    ENTERPRISE = const(2)

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        esp,
        secrets,
        attempts=2,
        connection_type=NORMAL,
        debug=False,
    ):
        """
        :param ESP_SPIcontrol esp: The ESP object we are using
        :param dict secrets: The WiFi and Adafruit IO secrets dict (See examples)
        :param status_pixel: (Optional) The pixel device - A NeoPixel, DotStar,
            or RGB LED (default=None)
        :param int attempts: (Optional) Failed attempts before resetting the ESP32 (default=2)
        :param const connection_type: (Optional) Type of WiFi connection: NORMAL or ENTERPRISE
        """
        # Read the settings
        self.esp = esp
        self.debug = debug
        self.ssid = secrets["ssid"]
        self.password = secrets.get("password", None)
        self.attempts = attempts
        self._connection_type = connection_type
        self._ap_index = 0

        # Check for WPA2 Enterprise keys in the secrets dictionary and load them if they exist
        if secrets.get("ent_ssid"):
            self.ent_ssid = secrets["ent_ssid"]
        else:
            self.ent_ssid = secrets["ssid"]
        if secrets.get("ent_ident"):
            self.ent_ident = secrets["ent_ident"]
        else:
            self.ent_ident = ""
        if secrets.get("ent_user"):
            self.ent_user = secrets["ent_user"]
        if secrets.get("ent_password"):
            self.ent_password = secrets["ent_password"]

    # pylint: enable=too-many-arguments

    def reset(self):
        """
        Perform a hard reset on the ESP32
        """
        if self.debug:
            print("Resetting ESP32")
        self.esp.reset()

    def connect(self):
        """
        Attempt to connect to WiFi using the current settings
        """
        if self.debug:
            if self.esp.status == esp32spi.WL_IDLE_STATUS:
                print("ESP32 found and in idle mode")
            print("Firmware vers.", self.esp.firmware_version)
            print("MAC addr:", [hex(i) for i in self.esp.MAC_address])
            for access_pt in self.esp.scan_networks():
                print(
                    "\t%s\t\tRSSI: %d"
                    % (str(access_pt["ssid"], "utf-8"), access_pt["rssi"])
                )
        if self._connection_type == ESPSPI_WiFiManager.NORMAL:
            self.connect_normal()
        elif self._connection_type == ESPSPI_WiFiManager.ENTERPRISE:
            self.connect_enterprise()
        else:
            raise TypeError("Invalid WiFi connection type specified")

    def _get_next_ap(self):
        if isinstance(self.ssid, (tuple, list)) and isinstance(
            self.password, (tuple, list)
        ):
            if not self.ssid or not self.password:
                raise ValueError("SSID and Password should contain at least 1 value")
            if len(self.ssid) != len(self.password):
                raise ValueError("The length of SSIDs and Passwords should match")
            access_point = (self.ssid[self._ap_index], self.password[self._ap_index])
            self._ap_index += 1
            if self._ap_index >= len(self.ssid):
                self._ap_index = 0
            return access_point
        if isinstance(self.ssid, (tuple, list)) or isinstance(
            self.password, (tuple, list)
        ):
            raise NotImplementedError(
                "If using multiple passwords, both SSID and Password should be lists or tuples"
            )
        return (self.ssid, self.password)

    def connect_normal(self):
        """
        Attempt a regular style WiFi connection
        """
        failure_count = 0
        (ssid, password) = self._get_next_ap()
        while not self.esp.is_connected:
            try:
                if self.debug:
                    print("Connecting to AP...")
                self.esp.connect_AP(bytes(ssid, "utf-8"), bytes(password, "utf-8"))
                failure_count = 0
            except (ValueError, RuntimeError) as error:
                print("Failed to connect, retrying\n", error)
                failure_count += 1
                if failure_count >= self.attempts:
                    failure_count = 0
                    (ssid, password) = self._get_next_ap()
                    self.reset()
                continue

    def create_ap(self):
        """
        Attempt to initialize in Access Point (AP) mode.
        Uses SSID and optional passphrase from the current settings
        Other WiFi devices will be able to connect to the created Access Point
        """
        failure_count = 0
        while not self.esp.ap_listening:
            try:
                if self.debug:
                    print("Waiting for AP to be initialized...")
                if self.password:
                    self.esp.create_AP(
                        bytes(self.ssid, "utf-8"), bytes(self.password, "utf-8")
                    )
                else:
                    self.esp.create_AP(bytes(self.ssid, "utf-8"), None)
                failure_count = 0
            except (ValueError, RuntimeError) as error:
                print("Failed to create access point\n", error)
                failure_count += 1
                if failure_count >= self.attempts:
                    failure_count = 0
                    self.reset()
                continue
        print("Access Point created! Connect to ssid:\n {}".format(self.ssid))

    def connect_enterprise(self):
        """
        Attempt an enterprise style WiFi connection
        """
        failure_count = 0
        self.esp.wifi_set_network(bytes(self.ent_ssid, "utf-8"))
        self.esp.wifi_set_entidentity(bytes(self.ent_ident, "utf-8"))
        self.esp.wifi_set_entusername(bytes(self.ent_user, "utf-8"))
        self.esp.wifi_set_entpassword(bytes(self.ent_password, "utf-8"))
        self.esp.wifi_set_entenable()
        while not self.esp.is_connected:
            try:
                if self.debug:
                    print(
                        "Waiting for the ESP32 to connect to the WPA2 Enterprise AP..."
                    )
                failure_count = 0
                sleep(1)
            except (ValueError, RuntimeError) as error:
                print("Failed to connect, retrying\n", error)
                failure_count += 1
                if failure_count >= self.attempts:
                    failure_count = 0
                    self.reset()
                continue

    def ping(self, host, ttl=250):
        """
        Pass the Ping request to the ESP32, update status LED, return response time

        :param str host: The hostname or IP address to ping
        :param int ttl: (Optional) The Time To Live in milliseconds for the packet (default=250)
        :return: The response time in milliseconds
        :rtype: int
        """
        if not self.esp.is_connected:
            self.connect()
        response_time = self.esp.ping(host, ttl=ttl)
        return response_time

    def ip_address(self):
        """
        Returns a formatted local IP address, update status pixel.
        """
        if not self.esp.is_connected:
            self.connect()
        return self.esp.pretty_ip(self.esp.ip_address)

    def signal_strength(self):
        """
        Returns receiving signal strength indicator in dBm
        """
        if not self.esp.is_connected:
            self.connect()
        return self.esp.rssi
