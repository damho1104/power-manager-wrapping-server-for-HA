#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import csv
import mimetypes
import atexit
import uvicorn

# from flask import *
# from cheroot.wsgi import Server
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse, FileResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

import lib
from lib import ConfigLoader, FileUtil, log

app = FastAPI(title="pm-wrap-server")

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
    uvicorn.run("lib:app",
                host=lib.configuration.get_ip(),
                port=int(lib.configuration.get_port()),
                reload=True,
                workers=100,
                access_log=False,
                log_level='info')


@app.middleware('http')
async def limit_remote_addr(request: Request, call_next):
    log.info(f'CLIENT: {request.client.host}:{request.client.port} / URL: {request.url}')
    ip_white_list = ConfigLoader().get_ip_whitelist()
    client_ip = str(request.client.host)
    if client_ip not in ip_white_list:
        raise HTTPException(status_code=403)  # Forbidden
    # Proceed if IP is allowed
    return await call_next(request)


@app.on_event('startup')
async def startup_event():
    log.init()
    log.info('START Server')


@app.on_event('shutdown')
async def shutdown_event():
    log.info('STOP Server')


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# @app.after_request
# def append_common_headers(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Methods'] = '*'
#     response.headers['Access-Control-Allow-Headers'] = '*'
#     response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
#     return response


# @app.errorhandler(404)
# def page_not_found(error):
#     return str(error), 404
#
#
# @app.errorhandler(Exception)
# def handle_exception(e):
#     log.error('An error occurred.', e)
#     return str(e), 500 if not hasattr(e, 'code') else e.code


@app.get('/favicon.ico')
def favicon():
    return send_resource('favicon.ico')


# @app.route('/<path:path>', methods=['GET'])
# def static_proxy(path):
#     return send_from_directory(FileUtil.get_path('html'), path)
#
#
def send_resource(*path):
    return FileResponse(FileUtil.get_path('html', *path))
