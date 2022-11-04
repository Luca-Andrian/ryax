#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pathlib
import shutil
import uuid


def handle(req):
    directory = pathlib.Path(req["directory"])
    path = f"/tmp/{uuid.uuid4()}-archive"
    archive_path = shutil.make_archive(
        path, "zip", str(directory.parent), directory.name
    )
    return {"archive": archive_path}
