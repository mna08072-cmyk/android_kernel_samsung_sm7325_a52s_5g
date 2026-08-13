#! /usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
# Copyright (c) 2011-2017, 2018 The Linux Foundation. All rights reserved.

# -*- coding: utf-8 -*-

# Invoke gcc, looking for warnings, and causing a failure if there are
# non-whitelisted warnings.

import errno
import re
import os
import sys
import subprocess

YELLOW='\033[33m'
RED='\033[31m'
RESET='\033[0m'

# Note that gcc uses unicode, which may depend on the locale.  TODO:
# force LANG to be set to en_US.UTF-8 to get consistent warnings.

allowed_warnings = set([
    "umid.c:138",
    "umid.c:213",
    "umid.c:388",
    "coresight-catu.h:116",
    "mprotect.c:42",
    "signal.c:95",
    "signal.c:51",
 ])

# Capture the name of the object file, can find it.
ofile = None

warning_re = re.compile(r'''(.*/|)([^/]+\.[a-z]+:\d+):(\d+:)? warning:''')
def color_print(text, color):
    print(color + text + RESET, end="")


def interpret_warning(line):
    text = line.decode(errors="replace")

    if "warning:" in text:
        color_print(text, YELLOW)
        return

    errors = [
        "error:",
        "fatal error:",
        "undefined reference",
        "cannot find",
        "No such file"
    ]

    if any(x in text for x in errors):
        color_print(text, RED)
        return

    print(text, end="")



def run_gcc():
    args = sys.argv[1:]
    # Look for -o
    try:
        i = args.index('-o')
        global ofile
        ofile = args[i+1]
    except (ValueError, IndexError):
        pass

    compiler = sys.argv[0]

    try:
        proc = subprocess.Popen(args, stderr=subprocess.PIPE)
        for line in proc.stderr:
            interpret_warning(line)

        result = proc.wait()
    except OSError as e:
        result = e.errno
        if result == errno.ENOENT:
            print(args[0] + ':',e.strerror)
            print('Is your PATH set correctly?')
        else:
            print(' '.join(args), str(e))

    return result

if __name__ == '__main__':
    status = run_gcc()
    sys.exit(status)
