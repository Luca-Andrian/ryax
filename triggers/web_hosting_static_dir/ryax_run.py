#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse


async def run(service, input_values: dict) -> None:

    if "ryax_endpoint_port" not in input_values:
        raise Exception(
            "Error: impossible to start the web server. Please set a endpoint to your Ryax workflow."
        )

    app = FastAPI()

    @app.middleware("http")
    async def crate_run_in_ryax(request: Request, call_next):
        response = await call_next(request)
        await service.create_run(
            {"ryax_headers": {key: value for key, value in request.headers.items()}}
        )
        return response

    # Redirect to index.html if not found
    @app.get(input_values["ryax_endpoint_prefix"])
    async def read_index():
        return RedirectResponse(
            url=input_values["ryax_endpoint_prefix"] + "/index.html"
        )

    app.mount(
        input_values["ryax_endpoint_prefix"],
        StaticFiles(directory=input_values["dir"]),
        name="static",
    )

    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        log_level="info",
        # Default the port and prefix are provided by Ryax in these two entries
        port=input_values["ryax_endpoint_port"],
    )
    server = uvicorn.Server(config)
    await server.serve()
