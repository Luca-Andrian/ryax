#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from google.cloud import storage

# Need help creating your authentication file? Follow the link below:
# https://cloud.google.com/storage/docs/reference/libraries#setting_up_authentication


def handle(req):
    # This env variable is used by storage.Client() to connect to gcp storage.
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = req["gcp_sto_creds"]
    client = storage.Client()
    bucket = client.get_bucket(req["gcp_sto_bucket"])

    # send file
    remote_file_path = os.path.join(
        req["dir_to_upload"], os.path.basename(req["file_to_upload"])
    )
    blob = bucket.blob(remote_file_path)
    blob.upload_from_filename(req["file_to_upload"])
    return {}
