#!/usr/bin/env python3

import logging
import re
import subprocess
import sys
from argparse import ArgumentParser

logging.basicConfig(format='%(message)s', level=logging.INFO)


def is_valid_message(commit_id='', repo_path='.'):
    """
    Validate commit messages according to Stacki commit message format:
        https://github.com/Teradata/stacki/wiki/Development#commit-message-format

    Assumes the following:
        - Stacki is cloned to a directory named 'stacki' (makes testing easier)
        - Script is run from the repository root

    :param commit_id: commit ID (for testing; default will validate HEAD)
    :param repo_path: current working directory (for testing)
    """

    result = subprocess.run(f'git show {commit_id} -s --format=%B'.split(),
                            encoding='utf-8', stdout=subprocess.PIPE, cwd=repo_path)
    message = result.stdout.strip()

    # merge commit
    if message.startswith('Merge'):
        logging.info('Merge commit\n')
        return True

    # README update
    if message.startswith('Update README.md'):
        logging.info('README update\n')
        return True

    # jira in oneline
    if re.search(r'^.*(STACKI-\d+|JIRA)', message):
        logging.info('JIRA mention in oneline\n')

    # prefix
    if not re.search(r'^(BUGFIX|INTERNAL|FEATURE|DOCS):', message):
        logging.info('No valid prefix\n')
        return False

    if '\n' in message:
        # blank line; regex: exactly one blank line after oneline
        if not re.search(r'^.+\n\n.+', message):
            logging.info('No single blank line after oneline\n')
            return False

        # jira in body
        if re.search(r'STACKI-\d+', message) and 'JIRA' not in message:
            logging.info('No JIRA mention in body when referencing ticket\n')
            return False

    logging.info('No special case\n')
    return True


def normal():
    ensure_git_repo()

    if is_valid_message():
        print('Pass')
        sys.exit(0)
    else:
        print('Fail')
        sys.exit(1)


# test with recent commits from a specified repository
def test(repo_path):
    ensure_git_repo(repo_path)

    result = subprocess.run('git log --format=format:%H'.split(),
                            encoding='utf-8', stdout=subprocess.PIPE, cwd=repo_path)
    for commit_id in result.stdout.strip().split()[:20]:
        logging.info(commit_id)
        print('Pass' if is_valid_message(commit_id=commit_id, repo_path=repo_path) else 'Fail')

    sys.exit(0)


def ensure_git_repo(repo_path='.'):
    try:
        if subprocess.run('git branch'.split(), stdout=subprocess.PIPE, cwd=repo_path).returncode == 128:
            sys.exit(1)
    except NotADirectoryError:
        sys.stderr.write(f'Invalid directory: {repo_path}')
        sys.exit(1)


def main():
    parser = ArgumentParser()
    parser.add_argument("--test_repo_path", help="test mode")
    args = parser.parse_args()

    if args.test_repo_path is None:
        normal()
    else:
        test(args.test_repo_path)


if __name__ == '__main__':
    main()
