#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def handle(mod_in):
    catfile = mod_in.get("file")
    content = ""
    with open(catfile, "r") as f:
        content += f.read()
    print("File content:")
    print(content)
    return {"stdout": content}
