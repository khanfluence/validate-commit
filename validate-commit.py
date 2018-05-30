#!/usr/bin/env python3

import re
import subprocess
import sys


def is_valid_message(commit=""):
    """
    Validate commit messages according to Stacki commit message format:
        https://github.com/Teradata/stacki/wiki/Development#commit-message-format

    Assume the following:
        - Stacki is cloned to a directory named "stacki" (makes testing easier)
        - Script is run from the repo root

    :param commit: commit ID for testing; default will validate HEAD
    """

    result = subprocess.run(f"git show {commit} -s --format=%B",
                            encoding="utf-8", shell=True,
                            stdout=subprocess.PIPE, cwd="..\stacki")
    message = result.stdout("utf-8").strip()

    # special pass cases
    if message.startswith("Merge") or message.startswith("Update README.md"):
        print("pass: ignore")  # expand, log
        return True

    # prefix
    if not re.search(r"^(BUGFIX|INTERNAL|FEATURE|DOCS):", message):
        print("fail: prefix")  # expand, log
        return False

    # multi-line cases
    if '\n' in message:
        # blank line; regex: exactly one blank line following oneline
        if not re.search(r".+\n\n.+", message):
            print("fail: blank line")  # expand, log
            return False

        # jira
        if re.search(r"STACKI-\d+", message) and "JIRA" not in message:
            print("fail: jira")  # expand, log
            return False

    print("pass")  # expand, log
    return True


print(is_valid_message())
