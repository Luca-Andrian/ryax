#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import apprise


def handle(req):
    apobj = apprise.Apprise()
    print("connecting")
    apobj.add(f'slack://{req["tokenA"]}/{req["tokenB"]}/{req["tokenC"]}')
    print(f"send notification {req['title']}")
    apobj.notify(
        title=req["title"],
        body=req["message"],
        notify_type=req["notify_type"],  # takes 'info', 'success', 'warning', 'failure'
    )
