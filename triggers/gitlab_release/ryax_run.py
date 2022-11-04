#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import functools
import json
import os
from typing import Dict

from aiohttp import web

from ryax_execution.ryax_source_protocol import RyaxSourceProtocol


class InvalidTokenException(BaseException):
    name: str = "Invalid Token"


class InvalidEventException(BaseException):
    name: str = "Invalid event"


async def receive_notification(request, service, input_values):
    try:
        if not request.headers.get("X-Gitlab-Token", "") == input_values.get(
            "secret_token"
        ):
            raise InvalidTokenException()

        data = await request.json()
        if not data["object_kind"] == "release":
            raise InvalidEventException()

        # Doc: https://docs.gitlab.com/ee/user/project/integrations/webhooks.html
        outputs = {
            "id": data["id"],
            "description": data["description"],
            "name": data["name"],
            "released_at": data["released_at"],
            "tag": data["tag"],
            "projectname": data["project"]["name"],
            "url": data["url"],
            "action": data["action"],
        }
        await service.create_run(outputs)
        return web.json_response({})
    except InvalidEventException as error:
        return web.json_response(error.name, status=400, dumps=json.dumps)
    except InvalidTokenException as error:
        return web.json_response(error.name, status=401, dumps=json.dumps)


async def run(service: RyaxSourceProtocol, input_values: Dict):
    runner = None
    try:
        app = web.Application()
        app.router.add_post(
            "/send",
            functools.partial(
                receive_notification, service=service, input_values=input_values
            ),
        )
        runner = web.AppRunner(app)
        await runner.setup()
        coroutine = web.TCPSite(
            runner, "0.0.0.0", os.environ.get("RYAX_SOURCE_PORT", "5002")
        )
        await coroutine.start()
    finally:
        if runner:
            await runner.cleanup()
