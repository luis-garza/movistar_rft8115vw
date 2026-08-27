"""Device tracker platform for the Movistar Askey RFT8115VW router."""

import logging

from homeassistant.components.device_tracker import ScannerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .client import MovistarDevice
from .coordinator import MovistarCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the device tracker platform from a config entry."""
    coordinator = MovistarCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    tracked_devices: dict[str, MovistarDeviceTracker] = {}

    @callback
    def _async_add_new_devices() -> None:
        """Create entities for newly discovered devices."""
        if coordinator.data is None:
            return

        new_entities: list[MovistarDeviceTracker] = []
        for mac in coordinator.data:
            if mac in tracked_devices:
                continue
            entity = MovistarDeviceTracker(coordinator, mac)
            tracked_devices[mac] = entity
            new_entities.append(entity)

        if new_entities:
            async_add_entities(new_entities)

    entry.async_on_unload(coordinator.async_add_listener(_async_add_new_devices))
    _async_add_new_devices()


class MovistarDeviceTracker(CoordinatorEntity[MovistarCoordinator], ScannerEntity):
    """Representation of a device connected to the router."""

    def __init__(self, coordinator: MovistarCoordinator, mac: str) -> None:
        """Initialize the device tracker entity."""
        super().__init__(coordinator)
        self._mac = mac
        self._attr_mac_address = mac

    @property
    def _device(self) -> MovistarDevice | None:
        """Return the device information, if available."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self._mac)

    @property
    def name(self) -> str:
        """Return the display name of the device."""
        device = self._device
        if device is not None and device.name:
            return device.name
        return self._mac

    @property
    def hostname(self) -> str | None:
        """Return the hostname of the device."""
        device = self._device
        if device is not None and device.name:
            return device.name
        return None

    @property
    def ip_address(self) -> str | None:
        """Return the IP address of the device."""
        device = self._device
        return device.ip if device is not None else None

    @property
    def is_connected(self) -> bool:
        """Return whether the device is currently connected."""
        return self.coordinator.is_device_connected(self._mac)

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Enable new device tracker entities by default."""
        return True
