#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import pathlib
import shutil
import uuid


def handle(req):
    zipfile = pathlib.Path(req["archive"])
    zipfile_name = zipfile.name.split(".")[0]
    to_directory = f"/tmp/{uuid.uuid4()}/{zipfile_name}"
    shutil.unpack_archive(zipfile, to_directory, "zip")
    if len(os.listdir(to_directory)) == 1:
        file = os.listdir(to_directory)[0]
        file_path = os.path.join(to_directory, file)
        dest_path = os.path.join(to_directory, zipfile_name)
        if os.path.isdir(file_path):
            if file == zipfile_name:
                pass
            else:
                os.rename(file_path, dest_path)
        to_directory = dest_path
    else:
        new_directory = f"/tmp/{uuid.uuid4()}/{zipfile_name}"
        shutil.move(to_directory, os.path.join(new_directory, zipfile_name))
        to_directory = new_directory
    return {"directory": to_directory}
