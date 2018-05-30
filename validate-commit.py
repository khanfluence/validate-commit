#!/usr/bin/env python3

import logging
import re
import subprocess
import sys

logging.basicConfig(format='%(message)s', level=logging.INFO)


def is_valid_message(commit_id=""):
    """
    Validate commit messages according to Stacki commit message format:
        https://github.com/Teradata/stacki/wiki/Development#commit-message-format

    Assumes the following:
        - Stacki is cloned to a directory named "stacki" (makes testing easier)
        - Script is run from the repo root

    :param commit_id: commit ID for testing; default will validate HEAD
    """

    result = subprocess.run(f"git show {commit_id} -s --format=%B",
                            encoding="utf-8", shell=True,
                            stdout=subprocess.PIPE, cwd="..\stacki")
    message = result.stdout.strip()

    # merge commit
    if message.startswith("Merge"):
        logging.info("Merge commit\n")
        return True

    # README update
    if message.startswith("Update README.md"):
        logging.info("README update\n")
        return True

    # jira in oneline
    if re.search(r"^.*(STACKI-\d+|JIRA)", message):
        logging.info("JIRA mention in oneline\n")

    # prefix
    if not re.search(r"^(BUGFIX|INTERNAL|FEATURE|DOCS):", message):
        logging.info("No valid prefix\n")
        return False

    if '\n' in message:
        # blank line; regex: exactly one blank line after oneline
        if not re.search(r"^.+\n\n.+", message):
            logging.info("No single blank line after oneline\n")
            return False

        # jira in body
        if re.search(r"STACKI-\d+", message) and "JIRA" not in message:
            logging.info("No JIRA mention in body when referencing ticket\n")
            return False

    logging.info("No special case\n")
    return True


def main():
    if len(sys.argv) == 1 or sys.argv[1] != "test":
        if is_valid_message():
            print("Pass")
            sys.exit(0)
        else:
            print("Fail")
            sys.exit(1)
    else:
        # test with recent commits
        result = subprocess.run("git log --format=format:%H",
                                encoding="utf-8", shell=True,
                                stdout=subprocess.PIPE, cwd="..\stacki")
        for commit_id in result.stdout.strip().split()[:20]:
            logging.info(commit_id)
            print("Pass" if is_valid_message(commit_id) else "Fail")

        sys.exit(0)


if __name__ == "__main__":
    main()
