
import json
import os
import sys
import time
from multiprocessing import Process

import requests
import websocket

from .objects import Key, Object


class ResponseError(Exception):
    pass


class Client():
    def __init__(self, callback):
        self.callback = callback
        self.host = os.getenv('GIMULATOR_HOST')
        if self.host is None:
            raise EnvironmentError
        self.id = os.getenv('CLIENT_ID')
        if self.id is None:
            raise EnvironmentError

        self.session = requests.Session()
        self.session.headers = {"Content-Type": "application/json"}
        self.register()
        self.ws_header = 'Cookie: token=' + \
            self.session.cookies.get_dict()['token']
        self.ws = websocket.WebSocket()
        self.p = Process(target=self.on_message)
        self.p.start()

    def on_message(self):
        while True:
            while True:
                try:
                    self.ws.connect(url=self.get_url('socket'),
                                    header=[self.ws_header])
                except ConnectionRefusedError:
                    self.p.terminate()
                except:
                    time.sleep(2)
                else:
                    break
            while True:
                try:
                    json_result = self.ws.recv()
                    result = json.loads(json_result)
                    self.callback(Object.from_dict(result))
                except KeyboardInterrupt:
                    self.p.terminate()
                    sys.exit(0)
                except:
                    break

    def get_url(self, endpoint):
        if endpoint == 'socket':
            return 'ws://' + self.host + '/' + endpoint
        return 'http://' + self.host + '/' + endpoint

    def register(self):
        data = json.dumps({"ID": self.id})
        response = self.session.post(
            self.get_url('register'), data=data)
        if response.status_code < 200 or response.status_code > 299:
            raise ResponseError(response.text)
        self.session.cookies = response.cookies

    def get(self, key: Key) -> Object:
        data = {
            'Key': key.__dict__,
            'Value': None
        }
        response = self.session.post(self.get_url(
            'get'), data=json.dumps(data))
        if response.status_code < 200 or response.status_code > 299:
            raise ResponseError(response.text)
        return Object.from_dict(json.loads(response.text))

    def set(self, obj: Object):
        data = {
            'Key': obj.Key.__dict__,
            'Value': obj.Value
        }
        response = self.session.post(self.get_url(
            'set'), data=json.dumps(data))
        if response.status_code < 200 or response.status_code > 299:
            raise ResponseError(response.text)

    def delete(self, obj: Object):
        data = {
            'Key': obj.Key.__dict__,
            'Value': obj.Value
        }
        response = self.session.post(self.get_url(
            'delete'), data=json.dumps(data))
        if response.status_code < 200 or response.status_code > 299:
            raise ResponseError(response.text)

    def find(self, key: Key) -> list:
        data = {
            'Key': key.__dict__,
            'Value': None
        }
        response = self.session.post(self.get_url(
            'find'), data=json.dumps(data))
        if response.status_code < 200 or response.status_code > 299:
            raise ResponseError(response.text)
        response = json.loads(response)
        result = []
        for item in response:
            result.append(Object.from_dict(item))
        return result

    def watch(self, key: Key):
        data = {
            'Key': key.__dict__,
            'Value': None
        }
        response = self.session.post(self.get_url(
            'watch'), data=json.dumps(data))
        if response.status_code < 200 or response.status_code > 299:
            raise ResponseError(response.text)
