#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def string_to_file(s: str, save_path: str = "/tmp/outfile.txt") -> str:
    with open(save_path, "w") as f:
        f.write(s)
    return save_path


def handle(inputs: dict = {}):
    s = inputs["instring"]
    out_path = string_to_file(s)
    return {"outfile": out_path}
