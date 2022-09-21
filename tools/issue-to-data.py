#!/usr/bin/env python3

import os
from datetime import date
from os.path import expanduser
from sys import argv

import yaml
from github import Github

import submission_process

if 'GITHUB_TOKEN' in os.environ:
    gh = Github(os.environ['GITHUB_TOKEN'])
else:
    with open(expanduser('~/.config/gh/hosts.yml')) as f:
        hosts = yaml.load(f, Loader=yaml.SafeLoader)
        gh = Github(hosts['github.com']['oauth_token'])

issue = gh.get_repo('daijia-database/data').get_issue(number=int(argv[1]))


def parse_issue(i):
    result = submission_process.parse(i.body)
    result['issue'] = i.number
    return result


parsed = parse_issue(issue)
submission_process.save(parsed, issue.title)
