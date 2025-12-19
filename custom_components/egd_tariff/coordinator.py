from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class EGDTariffCoordinator(DataUpdateCoordinator):
    """Coordinator for EG.D tariff data."""

    def __init__(self, hass: HomeAssistant):
        super().__init__(
            hass,
            _LOGGER,
            name="EG.D Tariff Coordinator",
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):
        """
        Fetch tariff data.

        ZATÍM jen placeholder – vrátíme statická data,
        aby integrace byla stabilní.
        """
        # TODO: tady později stáhneme data z EG.D
        return {
            "state": "NT",   # nebo "VT"
            "price_nt": 0.0,
            "price_vt": 0.0,
        }
