"""Movistar's Askey RFT8115VW router integration."""

import ast
import logging
import re

import homeassistant.helpers.config_validation as cv
import requests
import voluptuous as vol
from homeassistant.components.device_tracker import (
    PLATFORM_SCHEMA,
    DeviceScanner,
)
from homeassistant.const import CONF_HOST, CONF_PASSWORD

DOMAIN = "movistar_rft8115vw"

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_HOST): cv.string, vol.Required(CONF_PASSWORD): cv.string}
)


def get_scanner(hass, config):
    """Validate the configuration and return a scanner."""
    scanner = MovistarDeviceScanner(config["device_tracker"])
    return scanner if scanner.success_init else None


class MovistarDeviceScanner(DeviceScanner):
    """Looks for devices connected to a Movistar's Askey RFT8115VW router."""

    def __init__(self, config):
        """Initialize the scanner."""
        self.host = config[CONF_HOST]
        self.password = config[CONF_PASSWORD]
        self.parse_device_data = re.compile(r"var deviceData=([\w\W]+?);")
        self.url_initial = f"http://{self.host}"
        self.url_login = f"http://{self.host}/cgi-bin/te_acceso_router.cgi"
        self.url_map = f"http://{self.host}/te_mapa_red_local.asp"
        self.data_login = {
            "loginUsername": self.encode("1234"),
            "loginPassword": self.encode(self.password),
        }
        self.last_results = {}
        self.success_init = self._update_info()

    def scan_devices(self):
        """Scan for new devices and return a list with found device IDs."""
        self._update_info()
        return [item["mac"] for item in self.last_results]

    def get_device_name(self, device):
        """Return the name of the given device or None if it's unknown."""
        if not self.last_results:
            return None
        for item in self.last_results:
            if item["mac"] == device and "name" in item:
                return item["name"]
        return None

    def _update_info(self):
        """Ensure the information is up to date."""
        _LOGGER.info("Checking devices")
        devices = self.get_devices()
        if not devices:
            return False
        self.last_results = devices
        return True

    def encode(self, string):
        """Encode router login data."""
        return "".join(chr(ord(character) ^ 0x1F) for character in string)

    def get_devices(self):
        """Retrieve devices from the router."""
        _LOGGER.debug("Connecting to the router")
        session = requests.Session()
        response = session.get(self.url_initial)
        headers = session.cookies.get_dict()
        response = session.post(self.url_login, headers=headers, data=self.data_login)
        if response.ok:
            _LOGGER.debug("Connected to the router")
            devices = []
            _LOGGER.debug("Getting devices map from the router")
            response = session.get(self.url_map, headers=headers)
            if response.ok:
                for line in response.text.splitlines():
                    if self.parse_device_data.search(line):
                        _LOGGER.debug("Devices found in the map")
                        line_replaced = line.replace("\\", "")
                        devices_data = ast.literal_eval(
                            self.parse_device_data.search(line_replaced).group(1)
                        )
                        for device in devices_data:
                            if device[0] == "1":
                                devices.extend(
                                    [
                                        {
                                            "mac": device[6],
                                            "ip": device[3],
                                            "name": device[1],
                                        }
                                    ]
                                )
                        break
                if len(devices) == 0:
                    _LOGGER.warning("No devices found in the map")
            else:
                _LOGGER.error("Error getting devices map from the router")
                devices = None
        else:
            _LOGGER.error("Error connecting to the router")
            devices = None
        session.close()
        return devices
