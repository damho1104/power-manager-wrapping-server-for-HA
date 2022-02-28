#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import multiprocessing
import time

import requests
import lib
from flask import *
from lib.core import app
from lib import ConfigLoader, log
from collections import OrderedDict

device_status_lock = multiprocessing.Value('i', 0)


def request_to_power_manager_server(url: str, device_id: str):
    global device_status_lock
    with device_status_lock.get_lock():
        if lib.configuration.is_cert_mode(device_id=device_id):
            certs = lib.configuration.get_certs()
            verifies = lib.configuration.get_root_cert_path()
        else:
            certs = None
            verifies = None
        response = requests.get(url, cert=certs, verify=verifies)
        if response.status_code != 200:
            msg = f'status_code: {response.status_code} / {response.text}'
            result = False
        else:
            msg = response.json()
            result = True
        return result, msg


def get_server_ip_and_port(device_id: str):
    ip = lib.configuration.get_power_manager_server_ip(device_id=device_id)
    port = lib.configuration.get_power_manager_server_port(device_id=device_id)
    return ip, port


def get_device_status_from_pm(device_id: str):
    ip, port = get_server_ip_and_port(device_id)
    url = f'https://{ip}:{port}/device/status/{device_id}'
    return request_to_power_manager_server(url, device_id)


@app.route('/device/status/<device_id>')
def get_device_status(device_id):
    exclude_key_list = ['dayWatts', 'hourWatts', 'monthWatts', 'yearWatts']
    result, msg = get_device_status_from_pm(device_id)
    if not result:
        log.error(msg)
        abort(400, msg)
    result_dict: OrderedDict = msg
    for key in exclude_key_list:
        if result_dict.get(key, False):
            del result_dict[key]

    return jsonify(result_dict)


@app.route('/device/switch/<device_id>/On')
def get_device_on(device_id):
    ip, port = get_server_ip_and_port(device_id)
    url = f'https://{ip}:{port}/device/switch/{device_id}/On'
    result, msg = request_to_power_manager_server(url, device_id)
    if not result:
        log.error(msg)
        abort(400, msg)
    return jsonify(msg)


@app.route('/device/switch/<device_id>/Off')
def get_device_off(device_id):
    ip, port = get_server_ip_and_port(device_id)
    url = f'https://{ip}:{port}/device/switch/{device_id}/Off'
    result, msg = request_to_power_manager_server(url, device_id)
    if not result:
        log.error(msg)
        abort(400, msg)
    return jsonify(msg)


@app.route('/device/switch/<device_id>/status')
def get_switch_device_status(device_id):
    time.sleep(2)
    result, msg = get_device_status_from_pm(device_id)
    if not result:
        log.error(msg)
        abort(400, msg)
    result_dict: OrderedDict = msg
    result_value = {"on": True} if result_dict.get('switch') == 1 else {"on": False}
    return jsonify(result_value)


@app.route('/device/connection/<device_id>')
def get_connection_of_device(device_id):
    result, msg = get_device_status_from_pm(device_id)
    if not result:
        log.error(msg)
        abort(400, msg)
    result_dict: OrderedDict = msg
    result_value = "disconnected" if result_dict.get('switch') == 0 else "connected"
    return result_value

