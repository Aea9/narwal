import logging
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from .config_flow import MyPythonButtonsConfigFlow  # Asegúrate de que esto sea correcto
from .button import async_setup_entry  # Asegúrate de importar la función correctamente

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Narwal integration."""
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: config_entries.ConfigEntry):
    """Set up a config entry for Narwal."""
    await async_setup_entry(hass, config_entry)
    return True

# Registrar el flujo de configuración
config_entries.ConfigEntry.async_register(MyPythonButtonsConfigFlow)