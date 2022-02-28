#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import csv
import mimetypes
import atexit

from flask import *
from cheroot.wsgi import Server

import lib
from lib import ConfigLoader, FileUtil, log


# !! flask app
app = Flask('pm-server', root_path=FileUtil.get_path(), static_folder=FileUtil.get_path(os.path.join('html', 'static')))
app.config['TEMPLATES_AUTO_RELOAD'] = True  # reload templates if the cached version does not matches the template file.
server: Server = None

TYPES_FILENAME = 'mimetypes.csv'
if getattr(sys, 'frozen', False):
    types_file = FileUtil.get_path(TYPES_FILENAME)
else:
    types_file = FileUtil.get_path('res', TYPES_FILENAME)

with open(types_file, encoding='utf-8') as f:
    reader = csv.reader(f)
    lines = list(reader)

for line in lines:
    try:
        name, mime_type, extension = line
        mimetypes.add_type(type=mime_type, ext=extension)
    except:
        print(str(line))
        pass


def run():
    global server
    lib.configuration = ConfigLoader()
    # app.run(host=lib.configuration.get_ip(), port=lib.configuration.get_port())
    server = Server(bind_addr=(lib.configuration.get_ip(), int(lib.configuration.get_port())),
                    wsgi_app=app,
                    numthreads=100)
    try:
        atexit.register(shutdown_server)
        server.start()
    except KeyboardInterrupt:
        server.stop()


def shutdown_server():
    global server
    try:
        server.stop()
    except:
        pass


@app.before_request
def limit_remote_addr():
    ip_white_list = ConfigLoader().get_ip_whitelist()
    if request.remote_addr not in ip_white_list:
        abort(403)  # Forbidden


@app.after_request
def append_common_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
    return response


@app.errorhandler(404)
def page_not_found(error):
    return str(error), 404


@app.errorhandler(Exception)
def handle_exception(e):
    log.error('An error occurred.', e)
    return str(e), 500 if not hasattr(e, 'code') else e.code


@app.route('/favicon.ico')
def favicon():
    return send_resource('favicon.ico')


# @app.route('/<path:path>', methods=['GET'])
# def static_proxy(path):
#     return send_from_directory(FileUtil.get_path('html'), path)


def send_resource(*path):
    return send_file(FileUtil.get_path('html', *path))
