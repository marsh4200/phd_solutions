import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, DEFAULT_HOST, DEFAULT_PORT
from .controller import PHDController

class PHDConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            host = user_input.get("host", DEFAULT_HOST)
            port = user_input.get("port", DEFAULT_PORT)
            controller = PHDController(host, port)

            try:
                await controller.async_test_connection()
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=f"PHD 4K444 ({host})",
                    data=user_input,
                )

        data_schema = vol.Schema({
            vol.Required('host', default=DEFAULT_HOST): str,
            vol.Required('port', default=DEFAULT_PORT): int,
        })
        return self.async_show_form(step_id='user', data_schema=data_schema, errors=errors)

    async def async_step_options(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title='', data=user_input)

        data_schema = vol.Schema({
            vol.Required('debug', default=False): bool,
        })
        return self.async_show_form(step_id='options', data_schema=data_schema)
