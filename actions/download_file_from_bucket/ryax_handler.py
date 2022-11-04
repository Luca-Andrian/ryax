#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from enum import Enum

import boto3


class MatchEnum(Enum):
    earliest: str = "Earliest"
    latest: str = "Latest"
    exact: str = "Exact"


def connect_to_bucket(name: str, access_key: str, secret_key: str):
    s3 = boto3.resource(
        "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key
    )
    return s3.Bucket(name)


def handle(req):
    access_key: str = req.get("key_id")
    secret_key: str = req.get("secret_key_id")
    bucket_name: str = req.get("bucket_name")
    match: MatchEnum = req.get("match")
    key: str = req.get("key")

    my_bucket = connect_to_bucket(bucket_name, access_key, secret_key)

    all_objs = list(my_bucket.objects.filter(Prefix=key))

    if match == "Earliest":
        obj_to_download = min(all_objs, key=lambda x: x.last_modified)

    elif match == "Latest":
        obj_to_download = max(all_objs, key=lambda x: x.last_modified)

    else:
        for obj in all_objs:
            if obj.key == key:
                obj_to_download = obj
                break
        else:
            print(f"Could not find exact key: {key}, returning")
            return {}

    my_bucket.download_file(obj_to_download.key, "/tmp/" + str(obj_to_download.key))
    return {"output_data": "/tmp/" + str(obj_to_download.key)}
