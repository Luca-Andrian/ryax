#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import requests

def handle():
    response = requests.get('http://51.178.136.185:80/moodle/login/token.php?username=ryax_user&password=zWCD3HjpeTgQrMa-&service=ryaxService')
    return response.json()
