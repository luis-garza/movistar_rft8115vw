"""Config flow for the Movistar Askey RFT8115VW router integration."""

import logging

import voluptuous as vol
from aiohttp import ClientError
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.helpers import config_validation as cv

from .client import (
    CannotConnectError,
    InvalidAuthError,
    MovistarRouterClient,
    create_router_session,
)
from .const import (
    CONF_CONSIDER_HOME,
    CONF_INTERVAL_SECONDS,
    DEFAULT_CONSIDER_HOME,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

_STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)


class MovistarConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Movistar Askey RFT8115VW router."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, str] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                await self._async_test_connection(user_input)
            except InvalidAuthError:
                errors["base"] = "invalid_auth"
            except (CannotConnectError, ClientError, TimeoutError):
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_HOST], data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=_STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def _async_test_connection(self, user_input: dict[str, str]) -> None:
        """Test the connection to the router and the credentials."""
        session = create_router_session(self.hass, auto_cleanup=False)
        client = MovistarRouterClient(
            session, user_input[CONF_HOST], user_input[CONF_PASSWORD]
        )
        try:
            await client.async_get_devices()
        finally:
            session.detach()

    @staticmethod
    def async_get_options_flow(
        _config_entry: ConfigEntry,
    ) -> OptionsFlow:
        """Get the options flow for this handler."""
        return MovistarOptionsFlowHandler()


class MovistarOptionsFlowHandler(OptionsFlow):
    """Handle options for the Movistar Askey RFT8115VW router integration."""

    async def async_step_init(
        self, user_input: dict[str, int] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_INTERVAL_SECONDS,
                        default=self.config_entry.options.get(
                            CONF_INTERVAL_SECONDS, DEFAULT_SCAN_INTERVAL
                        ),
                    ): cv.positive_int,
                    vol.Required(
                        CONF_CONSIDER_HOME,
                        default=self.config_entry.options.get(
                            CONF_CONSIDER_HOME, DEFAULT_CONSIDER_HOME
                        ),
                    ): cv.positive_int,
                }
            ),
        )
