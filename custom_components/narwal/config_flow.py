import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

# Define los campos que el usuario deberá ingresar
DATA_SCHEMA = vol.Schema({
    vol.Required("email"): str,
    vol.Required("password"): str,
    vol.Required("secret_id"): str,
    vol.Required("device_id"): str,
    vol.Required("device_password"): str,
    vol.Required("otro"): str
})

class MyPythonButtonsConfigFlow(config_entries.ConfigFlow, domain="narwal"):
    """Manejador del flujo de configuración para Narwal."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Primer paso en el flujo de configuración."""
        if user_input is not None:
            # Guardar los datos ingresados por el usuario
            return self.async_create_entry(title="Narwal", data=user_input)

        # Si no hay datos ingresados, mostrar el formulario
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    """Manejo de las opciones de configuración adicionales."""

    def __init__(self, config_entry):
        """Inicializa el manejador de opciones."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Gestiona la inicialización del flujo de opciones."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(step_id="init", data_schema=DATA_SCHEMA)
