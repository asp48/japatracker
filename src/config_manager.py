import configparser
import os
from typing import Any

config_mgr = None

DEFAULT_CONFIG_PATH = "configs/config.ini"


class ConfigManager:

    def __init__(self, override_file_path=None):
        self.__config = configparser.ConfigParser()
        self.__config.read(DEFAULT_CONFIG_PATH)
        if override_file_path is not None:
            override_config = configparser.ConfigParser()
            override_config.read(override_file_path)
            self.__config.read_dict(override_config)
        self.__init_properties()

    def __init_properties(self):
        self.input_dir = self.__config['io']['input_dir']
        self.output_dir = self.__config['io']['output_dir']
        self.read_online = {"true": True, "false": False}.get(
            self.__config['mock-config']['read_online'].lower(), False)
        self.write_online = {"true": True, "false": False}.get(
            self.__config['mock-config']['write_online'].lower(), False)

    def __get(self, section, key) -> Any:
        return self.__config[section][key]

    def __get_whatsapp_property(self, key):
        return self.__get("whatsapp-config", key)

    def __get_drive_property(self, key):
        return self.__get("drive-config", key)

    def get_whatsapp_read_mode(self):
        return self.__get_whatsapp_property("read_mode")

    def get_whatsapp_group_name(self):
        return self.__get_whatsapp_property("group_name")

    def get_whatsapp_input_file(self):
        return os.path.join(self.input_dir, self.__get_whatsapp_property("chats_file_path"))

    def get_browser(self):
        return self.__get("browser-config", "browser")

    def get_drive_input_folder_id(self):
        return self.__get_drive_property("input_folder_id")

    def get_drive_output_folder_id(self):
        return self.__get_drive_property("output_folder_id")

    def get_drive_master_sheet_id(self):
        return self.__get_drive_property("master_sheet_id")


def get_instance(config_file_path=None) -> ConfigManager:
    global config_mgr
    if not config_mgr:
        config_mgr = ConfigManager(config_file_path)
    return config_mgr
