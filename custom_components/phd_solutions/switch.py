import asyncio
import logging

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN, CONF_INPUTS, CONF_OUTPUTS

_LOGGER = logging.getLogger(__name__)

POWER_COMMANDS = [
    ("power_on", "Matrix Power On", "s power 1!"),
    ("power_off", "Matrix Power Off", "s power 0!"),
]


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    controller = data["controller"]

    inputs = data.get(CONF_INPUTS, 4)
    outputs = data.get(CONF_OUTPUTS, 4)

    entities = []

    for input_num in range(1, inputs + 1):
        for output_num in range(1, outputs + 1):
            key = f"input_{input_num}_output_{output_num}"
            name = f"Input {input_num} → Output {output_num}"
            cmd = f"s in {input_num} av out {output_num}!"
            entities.append(PHDPushButton(controller, key, name, cmd))

    for key, name, cmd in POWER_COMMANDS:
        entities.append(PHDPushButton(controller, key, name, cmd))

    async_add_entities(entities, True)


class PHDPushButton(SwitchEntity):
    def __init__(self, controller, key, name, cmd):
        self._controller = controller
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"phd_matrix_{key}_{controller.host}"
        self._cmd = cmd
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        try:
            await self._controller.send_command(self._cmd)
            self._is_on = True
            self.async_write_ha_state()
            await asyncio.sleep(0.4)
            self._is_on = False
            self.async_write_ha_state()
        except Exception as err:
            _LOGGER.error("Command failed for %s: %s", self._cmd, err)

    async def async_turn_off(self, **kwargs):
        pass