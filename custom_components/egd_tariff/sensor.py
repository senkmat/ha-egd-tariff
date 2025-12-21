import logging
import async_timeout
import aiohttp
from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

HDO_CODE = "A1B6DP5"
REGION = "jih"
API_URL = f"https://java.egd.cz/hdo/api/v2/hdo-times-for-code-or-ean?code={HDO_CODE}&region={REGION}"

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Nastavení senzoru z configuration.yaml."""
    async_add_entities([EGDTariffSensor(HDO_CODE)], True)

class EGDTariffSensor(SensorEntity):
    def __init__(self, hdo_code):
        self._hdo_code = hdo_code
        self._state = "Unknown"
        self._attributes = {
            "hdo_code": hdo_code,
            "today_intervals": [],
            "last_update": None
        }
        self._old_intervals = None

    @property
    def name(self): return "EG.D HDO Tarif"

    @property
    def state(self): return self._state

    @property
    def extra_state_attributes(self):
        attrs = self._attributes.copy()
        # Přidání ceny z pomocníků
        nt_price = self.hass.states.get("input_number.cena_nt")
        vt_price = self.hass.states.get("input_number.cena_vt")
        if nt_price and vt_price:
            attrs["current_price"] = float(nt_price.state) if self._state == "NT" else float(vt_price.state)
        return attrs

    async def async_update(self):
        session = async_get_clientsession(self.hass)
        try:
            async with async_timeout.timeout(10):
                response = await session.get(API_URL)
                data = await response.json()
        except Exception as e:
            _LOGGER.error("EG.D API Error: %s", e)
            return

        if not data or "times" not in data: return

        new_intervals = data["times"][0].get("intervals", [])
        
        # Logika notifikace při změně času
        if self._old_intervals is not None and new_intervals != self._old_intervals:
            self.hass.bus.fire("egd_schedule_changed", {"new_schedule": new_intervals})
        
        self._old_intervals = new_intervals
        self._attributes["today_intervals"] = [f"{i['from']}-{i['to']}" for i in new_intervals]
        self._attributes["last_update"] = datetime.now().strftime("%H:%M:%S")

        # Výpočet zda je teď NT
        now = datetime.now().time()
        is_nt = False
        for i in new_intervals:
            start = datetime.strptime(i["from"], "%H:%M").time()
            end = datetime.strptime(i["to"], "%H:%M").time()
            if start <= end:
                if start <= now <= end: is_nt = True
            else: # Interval přes půlnoc
                if now >= start or now <= end: is_nt = True
        
        self._state = "NT" if is_nt else "VT"
