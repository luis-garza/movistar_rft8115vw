"""Data update coordinator for the Movistar Askey RFT8115VW router."""

import logging
from datetime import datetime, timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .client import (
    CannotConnectError,
    InvalidAuthError,
    MovistarDevice,
    MovistarRouterClient,
    create_router_session,
)
from .const import (
    CONF_CONSIDER_HOME,
    CONF_INTERVAL_SECONDS,
    DEFAULT_CONSIDER_HOME,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class MovistarCoordinator(DataUpdateCoordinator[dict[str, MovistarDevice]]):
    """Coordinate polling of the router for connected devices."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self._client = MovistarRouterClient(
            create_router_session(hass),
            entry.data[CONF_HOST],
            entry.data[CONF_PASSWORD],
        )
        self._last_seen: dict[str, datetime] = {}
        self._consider_home = timedelta(
            seconds=entry.options.get(CONF_CONSIDER_HOME, DEFAULT_CONSIDER_HOME)
        )
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                seconds=entry.options.get(CONF_INTERVAL_SECONDS, DEFAULT_SCAN_INTERVAL)
            ),
        )

    def is_device_connected(self, mac: str) -> bool:
        """Return whether a device is considered connected (within consider_home)."""
        if (last_seen := self._last_seen.get(mac)) is None:
            return False
        return dt_util.utcnow() - last_seen <= self._consider_home

    async def _async_update_data(self) -> dict[str, MovistarDevice]:
        """Fetch the list of connected devices from the router."""
        try:
            devices = await self._client.async_get_devices()
        except (CannotConnectError, InvalidAuthError) as err:
            raise UpdateFailed(str(err)) from err

        now = dt_util.utcnow()
        for device in devices:
            self._last_seen[device.mac] = now

        merged = dict(self.data or {})
        for device in devices:
            merged[device.mac] = device
        return merged
