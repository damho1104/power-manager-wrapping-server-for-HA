#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lib.util import log
import colorama
from colorama import Fore

colorama.init()


class Console:
    @staticmethod
    def title_message(msg: str):
        print(f'{Fore.GREEN}{msg}{Fore.RESET}')
        log.console(msg)

    @staticmethod
    def normal_message(msg: str):
        print(f'{Fore.LIGHTWHITE_EX}{msg}{Fore.RESET}')
        log.console(msg)

    @staticmethod
    def info_message(msg: str):
        print(f"{Fore.MAGENTA}{msg}{Fore.RESET}")
        log.console(msg)

    @staticmethod
    def check_message(msg: str, indent=1):
        indent_str = ''
        for inx in range(indent):
            indent_str += '-'
        print(f"{Fore.LIGHTWHITE_EX}{indent_str} {msg}{Fore.RESET}")
        log.console(f'{indent_str} {msg}')

    @staticmethod
    def warn_message(msg: str):
        print(f"{Fore.LIGHTYELLOW_EX}[Warning] {msg}{Fore.RESET}")
        log.warning(f'{msg}')

    @staticmethod
    def error_message(msg: str):
        print(f"{Fore.RED}[Error] {msg}{Fore.RESET}")
        log.error(f'{msg}')
