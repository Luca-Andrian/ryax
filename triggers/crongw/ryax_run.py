#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import asyncio
import datetime
from typing import Dict

import crontab

from ryax_execution.ryax_source_protocol import RyaxSourceProtocol


async def run(service: RyaxSourceProtocol, input_values: Dict):
    foreach_cron = crontab.CronTab(input_values.get("foreach"))
    while True:
        sleeping_time = foreach_cron.next(default_utc=False)
        await asyncio.sleep(sleeping_time)
        await service.create_run({"time": datetime.datetime.now().timestamp()})
