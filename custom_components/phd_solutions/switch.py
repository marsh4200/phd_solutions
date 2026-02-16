import logging
import asyncio
from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

ROUTES = []
for i in range(1,5):
    for j in range(1,5):
        key = f"input_{i}_output_{j}"
        name = f"Input {i} → Output {j}"
        cmd = f"s in {i} av out {j}!"
        ROUTES.append((key, name, cmd))

POWER_COMMANDS = [
    ("power_toggle", "Matrix Power Toggle", "s power 1!"),
    ("power_on", "Matrix Power On", "s power 1!"),
    ("power_off", "Matrix Power Off", "s power 0!"),
]

async def async_setup_entry(hass, entry, async_add_entities):
    controller = hass.data[DOMAIN][entry.entry_id]['controller']
    entities = [PHDPushButton(controller, key, name, cmd) for key, name, cmd in ROUTES]
    # add power controls
    for key, name, cmd in POWER_COMMANDS:
        entities.append(PHDPushButton(controller, key, name, cmd))
    async_add_entities(entities, True)

class PHDPushButton(SwitchEntity):
    def __init__(self, controller, key, name, cmd):
        self._controller = controller
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"phd_4k444_{key}_{controller.host}"
        self._cmd = cmd
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        try:
            await self._controller.send_command(self._cmd)
            # momentary on for UI feedback
            self._is_on = True
            self.async_write_ha_state()
            await asyncio.sleep(0.6)
            self._is_on = False
            self.async_write_ha_state()
        except Exception as e:
            _LOGGER.error('Command failed for %s: %s', self._cmd, e)

    async def async_turn_off(self, **kwargs):
        # not used; momentary only
        pass
