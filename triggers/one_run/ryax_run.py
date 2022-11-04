#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import Dict

from ryax_execution.ryax_source_protocol import RyaxSourceProtocol


async def run(service: RyaxSourceProtocol, _input_values: Dict):
    await service.create_run({})
