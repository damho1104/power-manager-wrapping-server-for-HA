#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from collections import OrderedDict
from lib import FileUtil


class ConfigLoader:
    def __init__(self):
        self.config_path = FileUtil.get_path('config.json')
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(self.config_path)
        self.config_dict = FileUtil.get_json_content_from_path(self.config_path)
        self.default_server: OrderedDict = None

    def get_ip(self):
        return self.config_dict.get('ip', '0.0.0.0')

    def get_port(self):
        return self.config_dict.get('port', '18080')

    def get_device_dict(self) -> OrderedDict:
        return self.config_dict.get('devices', {})

    def get_server_name_by_device_id(self, device_id: str):
        return self.get_device_dict().get(device_id, '')

    def get_servers(self) -> OrderedDict:
        return self.config_dict.get('server', {})

    def get_default_server_dict(self) -> OrderedDict:
        if self.default_server is None:
            for server_name in self.get_server_name_list():
                server_info: OrderedDict = self.get_servers().get(server_name)
                if server_info.get("default", False):
                    self.default_server = server_info
                    break
            if self.default_server is None:
                self.default_server = self.config_dict.get(self.get_server_name_list()[0])
        return self.default_server

    def get_server_name_list(self) -> list:
        return self.get_servers().keys()

    def is_cert_mode(self, server_name: str = None, device_id: str = None):
        if device_id is not None:
            server_name = self.get_server_name_by_device_id(device_id)
        if not server_name or server_name not in self.get_server_name_list():
            return True
        return self.get_servers().get(server_name).get('use_cert', True)

    def _get_server_info(self, key: str, default: str,
                         server_name: str,
                         device_id: str,
                         use_default_server: bool):
        if device_id is not None:
            server_name = self.get_server_name_by_device_id(device_id)
        if server_name and server_name in self.get_server_name_list():
            return self.get_servers().get(server_name).get(key)
        if use_default_server:
            return self.default_server.get(key)
        return default

    def get_power_manager_server_ip(self, server_name: str = None, device_id: str = None, use_default: bool = None):
        return self._get_server_info('power_manager_server_ip', '192.168.0.91', server_name, device_id, use_default)

    def get_power_manager_server_port(self, server_name: str = None, device_id: str = None, use_default: bool = None):
        return self._get_server_info('power_manager_server_port', '443', server_name, device_id, use_default)

    def get_client_cert_path(self) -> str:
        return self.config_dict.get('certs', {}).get('client_cert_path', '')

    def get_client_cert_key_path(self) -> str:
        return self.config_dict.get('certs', {}).get('client_cert_key_path', '')

    def get_root_cert_path(self) -> str:
        return self.config_dict.get('certs', {}).get('root_cert_path', None)

    def get_ip_whitelist(self):
        return self.config_dict.get('ip_whitelist', ['localhost', '127.0.0.1', '192.168.0.96'])

    def get_certs(self):
        return self.get_client_cert_path(), self.get_client_cert_key_path()
