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
        [
            EGDTariffStateSensor(coordinator),
            EGDTariffPriceSensor(
                coordinator,
                "nt_price",
                "EG.D NT Price",
                "egd_nt_price",
            ),
            EGDTariffPriceSensor(
                coordinator,
                "vt_price",
                "EG.D VT Price",
                "egd_vt_price",
            ),
            EGDTariffPriceSensor(
                coordinator,
                "current_price",
                "EG.D Current Price",
                "egd_current_price",
            ),
        ],
        update_before_add=True,
    )
