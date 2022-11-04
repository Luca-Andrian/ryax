#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import getpass
import os
import stat


def get_environment_vars():
    ret = ""
    for k, v in os.environ.items():
        ret += "\t{}: {}\n".format(k, v)
    return ret


def check_dir(d: str):
    return "d" if stat.S_ISDIR(d.st_mode) else "-"


def get_dir_stat_string(st):
    return str(oct(st.st_mode)[-3:])


def permissions_to_unix_name(st):
    p = {"7": "rwx", "6": "rw-", "5": "r-x", "4": "r--", "0": "---"}
    return check_dir(st) + "".join(p.get(x, x) for x in get_dir_stat_string(st))


def treat_dir(pth, contents, s=""):
    for item in contents:
        item_stats = os.stat(pth + "/" + item)
        s += "\t\t{}  {}\n".format(permissions_to_unix_name(item_stats), item)
    return "\t{}\n".format(pth) + s


def get_dirs_files_privileges():
    ret = ""
    for (pardir, dirs, files) in os.walk(os.getcwd()):
        ret += treat_dir(pardir, dirs + files)
    return ret


def handle(inputs: dict = {}):
    print(
        f"User: {getpass.getuser()}\nWorking Directory: {os.getcwd()}\nEnvironment Variables:\n{get_environment_vars()}\nUser Directories and Files:\n{get_dirs_files_privileges()}"
    )
