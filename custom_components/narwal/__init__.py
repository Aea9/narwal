import logging
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from .button import async_setup_entry

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Configura el componente durante la inicialización de Home Assistant."""
    _LOGGER.info("Iniciando el componente Narwal")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry):
    """Configura una entrada de configuración."""
    _LOGGER.info("Configurando la entrada: %s", entry.title)

    # Asegúrate de que llamas a async_setup_entry de button.py
    await async_setup_entry(hass, entry)

    return True

class MyPythonButtonsConfigFlow(config_entries.ConfigFlow, domain="narwal"):
    """Maneja la configuración de la integración."""

    async def async_step_user(self, user_input=None):
        """Paso inicial para solicitar información al usuario."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=self._get_data_schema(),
            )

        # Aquí puedes manejar la validación de los datos ingresados
        # y proceder a crear la entrada si todo es válido.
        return self.async_create_entry(title="Narwal", data=user_input)

    def _get_data_schema(self):
        """Devuelve el esquema de datos para el formulario."""
        from homeassistant.helpers import config_entry_flow
        from homeassistant import data_entry_flow

        return {
            # Define aquí los campos necesarios para la configuración
            # Ejemplo:
            "email": str,
            "password": str,
            "secret_id": str,
            "device_id": str,
            "device_password": str,
            "otro": str
        }
