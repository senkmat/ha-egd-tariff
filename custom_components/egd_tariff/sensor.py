from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import DOMAIN
from .coordinator import EGDTariffCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = EGDTariffCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        [EGDTariffStateSensor(coordinator)],
        update_before_add=True,
    )


class EGDTariffStateSensor(
    CoordinatorEntity, SensorEntity
):
    """Sensor showing NT / VT state."""

    _attr_name = "EG.D Tariff State"
    _attr_icon = "mdi:flash"

    def __init__(self, coordinator: EGDTariffCoordinator):
        super().__init__(coordinator)
        self._attr_unique_id = "egd_tariff_state"

    @property
    def native_value(self):
        return self.coordinator.data["state"]
