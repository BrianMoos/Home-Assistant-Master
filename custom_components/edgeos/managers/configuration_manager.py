from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PASSWORD, CONF_USERNAME

from ..helpers.const import *
from ..models.config_data import ConfigData
from .password_manager import PasswordManager


class ConfigManager:
    data: ConfigData
    config_entry: ConfigEntry
    password_manager: PasswordManager

    def __init__(self, password_manager: PasswordManager):
        self.password_manager = password_manager

    def update(self, config_entry: ConfigEntry):
        data = config_entry.data
        options = config_entry.options

        result = ConfigData()

        result.host = data.get(CONF_HOST)
        result.name = data.get(CONF_NAME)
        result.username = data.get(CONF_USERNAME)
        result.password = data.get(CONF_PASSWORD)
        result.unit = data.get(CONF_UNIT)

        result.monitored_devices = options.get(CONF_MONITORED_DEVICES, [])
        result.monitored_interfaces = options.get(CONF_MONITORED_INTERFACES, [])
        result.device_trackers = options.get(CONF_TRACK_DEVICES, [])
        result.update_interval = options.get(CONF_UPDATE_INTERVAL, 1)
        result.log_level = options.get(CONF_LOG_LEVEL, LOG_LEVEL_DEFAULT)
        result.log_incoming_messages = options.get(CONF_LOG_INCOMING_MESSAGES, False)

        if result.password is not None and len(result.password) > 0:
            result.password_clear_text = self.password_manager.decrypt(result.password)
        else:
            result.password_clear_text = result.password

        self.config_entry = config_entry
        self.data = result

    @staticmethod
    def _get_config_data_item(key, options, data):
        data_result = data.get(key, "")

        result = options.get(key, data_result)

        return result
