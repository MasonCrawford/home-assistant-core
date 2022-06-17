"""The lg_soundbar component."""
import logging

from homeassistant import config_entries, core
from homeassistant.const import CONF_HOST, CONF_PORT, Platform
from homeassistant.exceptions import ConfigEntryNotReady

from .config_flow import test_connect
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.MEDIA_PLAYER]


async def async_setup_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})
    # Verify the device is reachable with the given config before setting up the platform
    if CONF_HOST in entry.data.keys() and CONF_PORT in entry.data.keys():
        try:
            test_connect(entry.data[CONF_HOST], entry.data[CONF_PORT])
        except ConnectionError as err:
            raise ConfigEntryNotReady from err

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Unload a config entry."""
    result = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return result
