#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import asyncio
import datetime
from typing import Dict

from ryax_execution.ryax_source_protocol import RyaxSourceProtocol


def emit_time():
    return datetime.datetime.now().isoformat()


def time_to_seconds(time):
    times_seconds = {"days": 86400, "hours": 3600, "minutes": 60, "seconds": 1}
    total_time = 0.0
    for length, amt in time.items():
        total_time += times_seconds.get(length) * amt
    return total_time


async def run(service: RyaxSourceProtocol, input_values: Dict):
    print(input_values)
    time = {
        k: input_values[k]
        for k in input_values
        if k in ["days", "hours", "minutes", "seconds"]
    }
    every_seconds = time_to_seconds(time)
    while True:
        await service.create_run({"time": emit_time()})
        await asyncio.sleep(every_seconds)
