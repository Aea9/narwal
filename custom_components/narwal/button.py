from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from urllib import request
import json
import paho.mqtt.client as mqtt
import ssl
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Configurar el botón usando la configuración ingresada por el usuario."""
    email = config_entry.data.get("email")
    password = config_entry.data.get("password")
    secret_id = config_entry.data.get("secret_id")
    device_id = config_entry.data.get("device_id")
    device_password = config_entry.data.get("device_password")
    otro = config_entry.data.get("otro")

    # Obtener el token de autenticación
    data = json.dumps({
        "email": email,
        "password": password,
        "terminal_system_name": "iOS",
        "app_version": "2.6.5"
    }).encode()
    
    req = request.Request("https://de-idass.narwaltech.com/user-authentication-server/v2/login/loginByEmail", data=data)
    req.add_header('secret_id', secret_id)

    try:
        resp = request.urlopen(req)
        decodedResponse = json.loads(resp.read())
        authToken = decodedResponse["result"]["token"]
        uuid = decodedResponse["result"]["uuid"]
    except Exception as e:
        _LOGGER.error("Error en la autenticación: %s", e)
        return

    mqttc = create_mqtt_client(authToken, uuid)

    # Añadir los botones
    async_add_entities([
        MyPythonButton(hass, "Start", email, secret_id, device_id, device_password, mqttc, otro),
        MyPythonButton(hass, "Stop", email, secret_id, device_id, device_password, mqttc, otro)
    ])

def create_mqtt_client(authToken: str, uuid: str):
    """Crea y retorna un cliente MQTT configurado."""
    clientId = f"app_{uuid}_homeassistant"
    mqttc = mqtt.Client(client_id=clientId)
    mqttc.tls_set(certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE)
    mqttc.username_pw_set("", authToken)

    try:
        mqttc.connect("de-mqtt.narwaltech.com", 8883, 60)
    except Exception as e:
        _LOGGER.error("Error al conectar a MQTT: %s", e)

    return mqttc

class MyPythonButton(ButtonEntity):
    def __init__(self, hass: HomeAssistant, name: str, email: str, secret_id: str, device_id: str, device_password: str, mqttc, otro):
        self._hass = hass
        self._name = name
        self._email = email
        self._secret_id = secret_id
        self._device_id = device_id
        self._device_password = device_password
        self._mqttc = mqttc
        self._otro = otro

    @property
    def name(self):
        """Retorna el nombre del botón."""
        return self._name

    async def async_press(self):
        """Acción a ejecutar cuando se presiona el botón."""
        _LOGGER.info(f"Presionado: {self._name}")
        
        if self._name == "Start":
            await self.run_start()
        elif self._name == "Stop":
            await self.run_home()

    async def run_start(self):
        returnToHomeName = f"/{self._device_id}/{self._device_password}/supply/recall"
        returnToHomePayload = (
            bytearray(b'\x01D\n "') + 
            self._otro.encode('utf-8') + 
            bytearray(b'"\x12 "') + 
            self._otro.encode('utf-8') + 
            bytearray(b'"')
        )

        try:
            self._mqttc.loop_start()
            self._mqttc.publish(returnToHomeName, returnToHomePayload)
        finally:
            self._mqttc.loop_stop()

        _LOGGER.info(f"Ejecutando Aspirar con email: {self._email}")

    async def run_home(self):
        cleanTopicName = f"/{self._device_id}/{self._device_password}/clean/start_clean"
        entireHousePayload = (
            bytearray(b'\x01D\n "') + 
            self._otro.encode('utf-8') + 
            bytearray(b'"\x12 "') + 
            self._otro.encode('utf-8') + 
            bytearray(b'\n&\x08\x01\x12\x1a\n\x02\x08\x03\x12\x12\x08\x02\x10\x02\x18\x01 \x02(\x010\x018\x01@\x01H\x00\x18\x00\x1a\x04\x08\x01(\x00(\x01')
        )

        try:
            self._mqttc.loop_start()
            self._mqttc.publish(cleanTopicName, entireHousePayload)
        finally:
            self._mqttc.loop_stop()

        _LOGGER.info(f"Ejecutando Casa con email: {self._email}")
