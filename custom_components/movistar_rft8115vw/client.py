"""Async client for the Movistar Askey RFT8115VW router."""

import ast
import logging
import re
from dataclasses import dataclass

from aiohttp import ClientError, ClientSession, CookieJar
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_create_clientsession

_LOGGER = logging.getLogger(__name__)

_DEVICE_DATA = re.compile(r"var deviceData=([\w\W]+?);")

_NUMBER_OF_DEVICE_FIELDS = 7


def create_router_session(
    hass: HomeAssistant, *, auto_cleanup: bool = True
) -> ClientSession:
    """Create an aiohttp session that accepts cookies from unsecure hosts."""
    return async_create_clientsession(
        hass, cookie_jar=CookieJar(unsafe=True), auto_cleanup=auto_cleanup
    )


class MovistarRouterError(Exception):
    """Base error for the Movistar router client."""


class CannotConnectError(MovistarRouterError):
    """Error raised when the router cannot be reached."""

    def __init__(self, message: str = "") -> None:
        """Initialize the error."""
        super().__init__(
            message or "Unable to connect to the Movistar Askey RFT8115VW router"
        )


class InvalidAuthError(MovistarRouterError):
    """Error raised when the router rejects the credentials."""

    def __init__(self, message: str = "") -> None:
        """Initialize the error."""
        super().__init__(
            message or "Failed to authenticate with the router, check the password"
        )


@dataclass
class MovistarDevice:
    """A device currently connected to the router."""

    mac: str
    ip: str
    name: str


class MovistarRouterClient:
    """Async client to fetch connected devices from the router."""

    def __init__(self, session: ClientSession, host: str, password: str) -> None:
        """Initialize the client."""
        self._session = session
        self._password = password
        self._base_url = f"http://{host}"

    @staticmethod
    def _encode(string: str) -> str:
        """Encode router login data."""
        return "".join(chr(ord(character) ^ 0x1F) for character in string)

    async def async_get_devices(self) -> list[MovistarDevice]:
        """Fetch the list of connected devices from the router."""
        try:
            return await self._async_fetch()
        except (ClientError, TimeoutError) as err:
            raise CannotConnectError(str(err)) from err

    async def _async_fetch(self) -> list[MovistarDevice]:
        """Perform the HTTP requests and parse the device map."""
        _LOGGER.debug("Connecting to the router")
        async with self._session.get(self._base_url) as response:
            response.raise_for_status()

        data = {
            "loginUsername": self._encode("1234"),
            "loginPassword": self._encode(self._password),
        }
        async with self._session.post(
            f"{self._base_url}/cgi-bin/te_acceso_router.cgi", data=data
        ) as response:
            if not response.ok:
                _LOGGER.error("Error connecting to the router: %s", response.status)
                raise CannotConnectError

        _LOGGER.debug("Getting devices map from the router")
        async with self._session.get(
            f"{self._base_url}/te_mapa_red_local.asp"
        ) as response:
            if not response.ok:
                _LOGGER.error(
                    "Error getting devices map from the router: %s", response.status
                )
                raise CannotConnectError
            text = await response.text()

        if _DEVICE_DATA.search(text) is None:
            _LOGGER.debug("Router map did not contain device data: %s", text[:200])
            raise InvalidAuthError

        return self._parse_devices(text)

    @staticmethod
    def _parse_devices(text: str) -> list[MovistarDevice]:
        """Parse the router's device data."""
        devices: list[MovistarDevice] = []
        for line in text.splitlines():
            if _DEVICE_DATA.search(line) is None:
                continue
            _LOGGER.debug("Devices found in the map")
            line_replaced = line.replace("\\", "")
            match = _DEVICE_DATA.search(line_replaced)
            if match is None:
                continue
            try:
                device_data = ast.literal_eval(match.group(1))
            except (ValueError, SyntaxError) as err:
                _LOGGER.warning("Failed to parse device data: %s", err)
                continue
            for device in device_data:
                if (
                    not isinstance(device, list | tuple)
                    or len(device) < _NUMBER_OF_DEVICE_FIELDS
                    or device[0] != "1"
                ):
                    continue
                devices.append(
                    MovistarDevice(
                        mac=str(device[6]).lower(),
                        ip=str(device[3]),
                        name=str(device[1]),
                    )
                )
            break

        if not devices:
            _LOGGER.warning("No devices found in the map")
        return devices
