#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import csv

import mysql.connector


def write_to_csv(filename: str, headers: list, rows: list) -> None:
    with open(filename, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)


def handle(module_input):
    name = module_input.get("name")
    host = module_input.get("host")
    username = module_input.get("username")
    password = module_input.get("password")
    query = module_input.get("query")

    conn = mysql.connector.connect(
        host=host, user=username, password=password, database=name
    )

    cursor = conn.cursor()
    rows = cursor.execute(query)
    rows = cursor.fetchall()

    save_location = "/tmp/query_result.csv"
    write_to_csv(save_location, list(cursor.column_names), rows)
    return {"result": save_location}
