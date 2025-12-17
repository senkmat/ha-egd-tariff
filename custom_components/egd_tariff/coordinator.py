from __future__ import annotations

from datetime import datetime, time, timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import DOMAIN, UPDATE_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)


from datetime import time, timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util


class EGDTariffCoordinator(DataUpdateCoordinator):
    def __init__(self, hass):
        super().__init__(
            hass,
            None,
            name="egd_tariff",
            update_interval=timedelta(seconds=60),
        )

    async def _async_update_data(self):
        now = dt_util.now().time()
        is_nt = time(0, 0) <= now < time(6, 0)

        return {
            "state": "NT" if is_nt else "VT"
        }
