from __future__ import annotations

from datetime import datetime, time, timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import DOMAIN, UPDATE_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)


class EGDTariffCoordinator(DataUpdateCoordinator):
    """Coordinator for EG.D tariff data."""

    def __init__(self, hass: HomeAssistant):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS),
        )

    async def _async_update_data(self):
        """Fetch NT/VT tariff data (temporary static logic)."""

        now = dt_util.now().time()

        # Dočasný NT rozpis (Brno – FAKE, jen pro logiku)
        nt_blocks = [
            (time(0, 0), time(6, 0)),
            (time(13, 0), time(15, 0)),
        ]

        is_nt = any(start <= now < end for start, end in nt_blocks)

        nt_price = 2.49
        vt_price = 4.89

        data = {
            "is_nt": is_nt,
            "state": "NT" if is_nt else "VT",
            "nt_blocks": nt_blocks,
            "nt_price": nt_price,
            "vt_price": vt_price,
            "current_price": nt_price if is_nt else vt_price,
            "last_update": datetime.now(),
        }

        _LOGGER.debug("EG.D tariff data updated: %s", data)

        return data
