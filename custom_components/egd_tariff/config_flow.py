from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


class EGDTariffConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for EG.D Tariff."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(
                title="EG.D Tariff (NT/VT)",
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required("distributor", default="EG.D"): str,
                vol.Required("tariff", default="A1B6DP5"): str,
                vol.Required("area", default="Brno"): str,
                vol.Optional("hdo_group", default="Nevím"): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )
