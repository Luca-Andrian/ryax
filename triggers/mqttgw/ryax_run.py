#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import asyncio
import socket
from dataclasses import dataclass
from typing import Dict

import paho.mqtt.client as mqtt

from ryax_execution.ryax_source_protocol import RyaxSourceProtocol


class AsyncioHelper:
    def __init__(self, loop, client):
        self.loop = loop
        self.client = client
        self.client.on_socket_open = self.on_socket_open
        self.client.on_socket_close = self.on_socket_close
        self.client.on_socket_register_write = self.on_socket_register_write
        self.client.on_socket_unregister_write = self.on_socket_unregister_write

    def on_socket_open(self, client, userdata, sock):
        def cb():
            client.loop_read()

        self.loop.add_reader(sock, cb)
        self.misc = self.loop.create_task(self.misc_loop())

    def on_socket_close(self, client, userdata, sock):
        self.loop.remove_reader(sock)
        self.misc.cancel()

    def on_socket_register_write(self, client, userdata, sock):
        def cb():
            client.loop_write()

        self.loop.add_writer(sock, cb)

    def on_socket_unregister_write(self, client, userdata, sock):
        self.loop.remove_writer(sock)

    async def misc_loop(self):
        while self.client.loop_misc() == mqtt.MQTT_ERR_SUCCESS:
            try:
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                break


@dataclass
class MQTTGateway:
    service: RyaxSourceProtocol
    input_values: Dict

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        if self.got_message:
            self.got_message.set_result(msg.payload)

    def on_disconnect(self, client, userdata, rc):
        self.disconnected.set_result(rc)

    async def handler(self):
        self.disconnected = asyncio.get_event_loop().create_future()
        self.got_message = asyncio.get_event_loop().create_future()

        self.topic = self.input_values.get("mqtt_topic")
        mqtt_server = self.input_values.get("mqtt_server")

        mqtt_client = mqtt.Client()

        mqtt_client.on_connect = self.on_connect
        mqtt_client.on_message = self.on_message
        mqtt_client.on_disconnect = self.on_disconnect

        AsyncioHelper(asyncio.get_event_loop(), mqtt_client)
        mqtt_client.connect(mqtt_server, 1883, 60)
        mqtt_client.socket().setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2048)

        while True:
            message = await self.got_message
            self.got_message = asyncio.get_event_loop().create_future()
            data = message.decode()
            await self.service.create_run({"value": data})


async def run(service: RyaxSourceProtocol, input_values: dict) -> None:
    MQTTGateway(service, input_values).handler()
