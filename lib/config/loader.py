#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from collections import OrderedDict
from lib import FileUtil, Console


class ConfigLoader:
    def __init__(self):
        self.config_path = FileUtil.get_path('config.json')
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(self.config_path)

        # Console.info_message(f'Load config(file: {self.config_path})')
        self.config_dict = FileUtil.get_json_content_from_path(self.config_path)

    def get_ip(self):
        return self.config_dict.get('ip', '0.0.0.0')

    def get_port(self):
        return self.config_dict.get('port', '18080')

    def get_power_manager_server_ip(self):
        return self.config_dict.get('power_manager_server_ip', '192.168.0.91')

    def get_power_manager_server_port(self):
        return self.config_dict.get('power_manager_server_port', '443')

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
