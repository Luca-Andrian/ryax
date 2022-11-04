#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
from requests.structures import CaseInsensitiveDict


def handle(req):
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    params = {"zapikey": req["token"]}
    data = {
        "text": req["message"],
        "bot": {
            "name": req["bot_name"],
            "image": req["bot_logo"],
        },
    }
    resp = requests.post(req["url"], headers=headers, params=params, data=str(data))
    print("Response:", resp.status_code)
