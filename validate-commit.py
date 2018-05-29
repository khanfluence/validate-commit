#!/usr/bin/env python3

import re
import subprocess


def is_valid_message(commit=None):

    print(message + "\n-----")

    # ignore
    if message.startswith("Merge") or message.startswith("Update README.md"):
        return "pass: ignore"

    # prefix
    if not re.search(r"^(BUGFIX|INTERNAL|FEATURE|RELEASE):", message):
        return "fail: prefix"

    # multi-line cases
    if '\n' in message:
        # blank line
        if not re.search(r"[^\n]+\n\n[^\n]+", message):
            return "fail: blank line"

        # jira
        if re.search(r"STACKI-\d\d\d", message) and "JIRA" not in message:
            return "fail: jira"

    return "pass"


print(is_valid_message())
