from __future__ import annotations

import logging
from datetime import datetime, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .tariffs import TARIFFS

_LOGGER = logging.getLogger(__name__)


class EGDTariffCoordinator(DataUpdateCoordinator):
    """Coordinator for EG.D tariff data."""

    def __init__(self, hass: HomeAssistant):
        super().__init__(
            hass,
            _LOGGER,
            name="EG.D Tariff Coordinator",
            update_interval=timedelta(minutes=1),
        )

        self._tariff = "A1B6DP5"
        self._region = "Brno"

    async def _async_update_data(self):
        now = datetime.now().time()
        intervals = TARIFFS[self._tariff][self._region]

        state = "VT"
        for start, end in intervals:
            if start <= end:
                if start <= now <= end:
                    state = "NT"
            else:
                # interval přes půlnoc
                if now >= start or now <= end:
                    state = "NT"

        return {
            "state": state,
            "price_nt": 0.0,   # připraveno do budoucna
            "price_vt": 0.0,
        }
