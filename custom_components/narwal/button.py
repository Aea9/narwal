from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Configurar el botón usando la configuración ingresada por el usuario."""
    email = config_entry.data.get("email")
    password = config_entry.data.get("password")
    secret_id = config_entry.data.get("secret_id")
    device_id = config_entry.data.get("device_id")
    device_password = config_entry.data.get("device_password")

    async_add_entities([
        MyPythonButton(hass, "Botón 1", email, password, secret_id, device_id, device_password),
        MyPythonButton(hass, "Botón 2", email, password, secret_id, device_id, device_password)
    ])

class MyPythonButton(ButtonEntity):
    def __init__(self, hass: HomeAssistant, name: str, email: str, password: str, secret_id: str, device_id: str, device_password: str):
        self._hass = hass
        self._name = name
        self._email = email
        self._password = password
        self._secret_id = secret_id
        self._device_id = device_id
        self._device_password = device_password

    @property
    def name(self):
        """Retorna el nombre del botón."""
        return self._name

    async def async_press(self):
        """Acción a ejecutar cuando se presiona el botón."""
        _LOGGER.info(f"Presionado: {self._name}")
        
        # Llamar a las funciones usando los datos de configuración
        if self._name == "Botón 1":
            await self.run_python_code_1()
        elif self._name == "Botón 2":
            await self.run_python_code_2()

    async def run_python_code_1(self):
        """Ejecuta código Python para el Botón 1."""
        _LOGGER.info(f"Ejecutando Botón 1 con email: {self._email}, password: {self._password}, secret_id: {self._secret_id}, device_id: {self._device_id}, device_password: {self._device_password}")
        # Aquí va tu código Python usando los valores configurados

    async def run_python_code_2(self):
        """Ejecuta código Python para el Botón 2."""
        _LOGGER.info(f"Ejecutando Botón 2 con email: {self._email}, password: {self._password}, secret_id: {self._secret_id}, device_id: {self._device_id}, device_password: {self._device_password}")
        # Aquí va tu código Python usando los valores configurados
