import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT

from .const import (
    DOMAIN,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_INPUTS,
    DEFAULT_OUTPUTS,
    CONF_INPUTS,
    CONF_OUTPUTS,
    CONF_MODEL,
)

from .controller import PHDController


class PHDConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for PHD Solutions."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            host = user_input.get(CONF_HOST, DEFAULT_HOST)
            port = user_input.get(CONF_PORT, DEFAULT_PORT)

            controller = PHDController(host, port)

            try:
                await controller.async_test_connection()
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                inputs = user_input.get(CONF_INPUTS, DEFAULT_INPUTS)
                outputs = user_input.get(CONF_OUTPUTS, DEFAULT_OUTPUTS)

                model = f"{inputs}x{outputs}"

                return self.async_create_entry(
                    title=f"PHD Solutions ({host})",
                    data={
                        CONF_HOST: host,
                        CONF_PORT: port,
                        CONF_INPUTS: inputs,
                        CONF_OUTPUTS: outputs,
                        CONF_MODEL: model,
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
                vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
                vol.Required(CONF_INPUTS, default=DEFAULT_INPUTS): vol.All(
                    int, vol.Range(min=1, max=16)
                ),
                vol.Required(CONF_OUTPUTS, default=DEFAULT_OUTPUTS): vol.All(
                    int, vol.Range(min=1, max=16)
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
