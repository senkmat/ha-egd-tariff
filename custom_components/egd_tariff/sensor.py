from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import EGDTariffCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = EGDTariffCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        [EGDTariffStateSensor(coordinator)],
        update_before_add=True,
    )


class EGDTariffStateSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "EG.D Tariff State"
    _attr_icon = "mdi:flash"
    _attr_unique_id = "egd_tariff_state"

    def __init__(self, coordinator):
        super().__init__(coordinator)

    @property
    def native_value(self):
        return self.coordinator.data["state"]
