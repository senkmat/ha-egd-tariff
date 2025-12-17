from __future__ import annotations

from datetime import datetime, time
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)
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
            update_interval=dt_util.timedelta(
                seconds=UPDATE_INTERVAL_SECONDS
            ),
        )

    async def _async_update_data(self):
        """Fetch tariff data (FAKE for now)."""
        now = dt_util.now().time()

        # FAKE NT schedule for Brno (example)
        nt_blocks = [
            (time(0, 0), time(6, 0)),
            (time(13, 0), time(15, 0)),
        ]

        is_nt = any(start <= now < end for start, end in nt_blocks)

        return {
            "is_nt": is_nt,
            "state": "NT" if is_nt else "VT",
            "nt_blocks": nt_blocks,
            "last_update": datetime.now(),
        }
