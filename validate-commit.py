import re
import subprocess


def is_valid_message():
    message = subprocess.run("git show -s --format=%B", shell=True, stdout=subprocess.PIPE, cwd="..\stacki")\
        .stdout.decode("utf-8").strip()

    # merge (ignore)
    if message.startswith("Merge"):
        return "pass: merge"

    # starts with
    if not re.search(r"^(BUGFIX|INTERNAL|FEATURE|RELEASE):", message):
        return "fail: starts with"

    # multi-line
    if '\n' in message:
        # blank line
        if not re.search(r"[^\n]+\n\n[^\n]+", message):
            return "fail: blank line"

        # jira
        if re.search(r"STACKI-\d\d\d", message) and "JIRA" not in message:
            return "fail: jira"

    return "pass"


print(is_valid_message())
