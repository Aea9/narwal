import logging
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

# Inicializa el logger
_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Configura la integración Narwal."""
    _LOGGER.info("Configurando la integración Narwal")
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: config_entries.ConfigEntry):
    """Configura una entrada de configuración para Narwal."""
    _LOGGER.info(f"Configurando la entrada Narwal: {config_entry.data}")

    # Almacena datos de configuración en hass.data
    hass.data.setdefault("narwal", {})
    hass.data["narwal"][config_entry.entry_id] = config_entry.data

    # Aquí puedes agregar la lógica para añadir las entidades, como botones
    # Asegúrate de que ya tengas la función async_add_entities definida correctamente
    await async_add_entities(hass, config_entry)

    return True

async def async_add_entities(hass: HomeAssistant, config_entry: config_entries.ConfigEntry):
    """Agrega las entidades para la integración Narwal."""
    from .button import MyPythonButton  # Asegúrate de que tu clase MyPythonButton esté correctamente importada

    # Obtén los datos de configuración
    email = config_entry.data.get("email")
    password = config_entry.data.get("password")
    secret_id = config_entry.data.get("secret_id")
    device_id = config_entry.data.get("device_id")
    device_password = config_entry.data.get("device_password")
    otro = config_entry.data.get("otro")

    # Crea las entidades de los botones
    async_add_entities([
        MyPythonButton(hass, "Botón 1", email, password, secret_id, device_id, device_password, otro),
        MyPythonButton(hass, "Botón 2", email, password, secret_id, device_id, device_password, otro)
    ])
