#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
from pathlib import Path

import boto3


def create_bucket_key(file_name, timestamp: bool):
    file_name = Path(file_name)
    if timestamp:
        date = datetime.datetime.now().isoformat()
        return file_name.stem + "_" + date + file_name.suffix
    return file_name.stem + file_name.suffix


def connect_to_bucket(name: str, access_key: str, secret_key: str):
    s3 = boto3.resource(
        "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key
    )
    return s3.Bucket(name)


def handle(req):
    access_key: str = req.get("key_id")
    secret_key: str = req.get("secret_key_id")
    bucket_name: str = req.get("bucket_name")
    file_name: str = req.get("file_to_upload")
    timestamp_bool: bool = (
        True if req.get("timestamp_bool").lower() == "timestamp" else False
    )

    my_bucket = connect_to_bucket(bucket_name, access_key, secret_key)
    file_upload_key = create_bucket_key(file_name, timestamp_bool)
    my_bucket.upload_file(file_name, file_upload_key)
    return {}
