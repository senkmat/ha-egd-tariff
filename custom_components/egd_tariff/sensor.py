import logging
import async_timeout
import aiohttp
from datetime import datetime, time
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

# Konfigurace
HDO_CODE = "A1B6DP5"
REGION = "jih"
API_URL = f"https://java.egd.cz/hdo/api/v2/hdo-times-for-code-or-ean?code={HDO_CODE}&region={REGION}"

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Nastavení senzoru při startu."""
    async_add_entities([EGDTariffSensor(HDO_CODE)], True)

class EGDTariffSensor(SensorEntity):
    """Senzor pro aktuální tarif EG.D."""

    def __init__(self, hdo_code):
        self._hdo_code = hdo_code
        self._state = "Unknown"
        self._attributes = {
            "hdo_code": hdo_code,
            "next_change": None,
            "today_intervals": [],
            "last_update": None,
            "schedule_changed": False
        }
        self._old_schedule = None

    @property
    def name(self):
        return "EG.D HDO Tarif"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        # Dynamicky přidáváme ceny z pomocníků, pokud existují
        # Vytvoř si v HA: input_number.cena_nt a input_number.cena_vt
        attrs = self._attributes.copy()
        
        state_nt = self.hass.states.get("input_number.cena_nt")
        state_vt = self.hass.states.get("input_number.cena_vt")
        
        if state_nt and state_vt:
            attrs["current_price"] = float(state_nt.state) if self._state == "NT" else float(state_vt.state)
        
        return attrs

    async def async_update(self):
        """Stáhne data a vyhodnotí stav."""
        session = async_get_clientsession(self.hass)
        
        try:
            async with async_timeout.timeout(10):
                response = await session.get(API_URL)
                data = await response.json()
        except Exception as e:
            _LOGGER.error("Chyba při stahování dat EG.D: %s", e)
            return

        if not data or "times" not in data:
            return

        # 1. Kontrola změny rozpisu (pro notifikace)
        new_schedule = data["times"][0].get("intervals", [])
        if self._old_schedule is not None and new_schedule != self._old_schedule:
            self._attributes["schedule_changed"] = True
            # Fire event, na který můžeš v HA navázat automatizaci pro notifikaci
            self.hass.bus.fire("egd_schedule_changed", {
                "hdo_code": self._hdo_code,
                "new_schedule": new_schedule
            })
        else:
            self._attributes["schedule_changed"] = False
        
        self._old_schedule = new_schedule
        self._attributes["today_intervals"] = new_schedule
        self._attributes["last_update"] = datetime.now().isoformat()

        # 2. Vyhodnocení aktuálního tarifu
        now_time = datetime.now().time()
        is_nt = False
        
        for interval in new_schedule:
            start = datetime.strptime(interval["from"], "%H:%M").time()
            end = datetime.strptime(interval["to"], "%H:%M").time()
            
            # Ošetření intervalů přes půlnoc
            if start <= end:
                if start <= now_time <= end:
                    is_nt = True
                    break
            else: # Např. 22:00 - 06:00
                if now_time >= start or now_time <= end:
                    is_nt = True
                    break

        self._state = "NT" if is_nt else "VT"
