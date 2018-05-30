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
    message = result.stdout.strip()

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
        if not re.search(r"^.+\n\n.+", message):
            print("fail: blank line")  # expand, log
            return False

        # jira
        if re.search(r"STACKI-\d+", message) and "JIRA" not in message:
            print("fail: jira")  # expand, log
            return False

    print("pass")  # expand, log
    return True


def main():
    if len(sys.argv) > 0 and sys.argv[1] == "test":
        result = subprocess.run("git log --format=format:%H",
                                encoding="utf-8", shell=True,
                                stdout=subprocess.PIPE, cwd="..\stacki")
        for commit in result.stdout.strip().split()[:50]:
            is_valid_message(commit)  # print commit message?
            # line after if?
    else:  # explicit else?
        is_valid_message()


if __name__ == "__main__":
    main()
