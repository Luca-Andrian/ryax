#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
import time

import requests
from influxdb import InfluxDBClient


def create_json_body(measurement, time, value):
    return [{"measurement": measurement, "time": time, "fields": {"value": value}}]


def handle(float2db_input):
    host = float2db_input.get("host")
    port = float2db_input.get("port")
    user = float2db_input.get("user")
    password = float2db_input.get("password")
    dbname = float2db_input.get("dbname")
    measurement_name = float2db_input.get("measurement_name")
    value = float2db_input.get("value")
    timestamp = datetime.datetime.now().isoformat()
    while True:
        try:
            client = InfluxDBClient(host, port, user, password, dbname)
            dbs = client.get_list_database()
            if not any([db["name"] == dbname for db in dbs]):
                client.create_database(dbname)
            client.switch_database(dbname)
            json_body = create_json_body(measurement_name, timestamp, value)
            client.write_points(json_body)
            client.close()
        except requests.exceptions.ConnectionError:
            print("Connection Error! Retrying...")
            time.sleep(1)
        else:
            break
    return {}
