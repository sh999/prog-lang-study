#!/usr/bin/env python3
#
# USAGE: issues.py <repo url> [--username <username> --password <password>]
# NOTE: Requires the GitHub Python library (`pip3 install PyGitHub`).

from argparse import ArgumentParser
from github import Github


def get_issues(repo_name):
    print('Retreiving issue data from "{0}"...'.format(repo_name))
    summary = ""
    try:
        repository = github.get_repo(repo_name)
        print("repo is found")
        issues = [issue for issue in repository.get_issues()]
        open = [issue for issue in issues if issue.state == 'open']
        closed = [issue for issue in issues if issue.state == 'closed']
        print("Issues:")

        print('{0} issues found. ({1} open, {2} closed)'.format(len(issues), len(open), len(closed)))
        summary = '{0} issues found. ({1} open, {2} closed)'.format(len(issues), len(open), len(closed))
        for issue in issues:
            print('#{0:04d} ({1}):\t{2}'.format(issue.number, issue.state, issue.title))
    except Exception as e:
        print("error: ", e)
        pass
    return summary

  
if __name__ == '__main__':
    parser = ArgumentParser(description='Analyze GitHub repository issues.')
    parser.add_argument('-u', '--username', help='The username to sign in with, if you need.')
    parser.add_argument('-p', '--password', help='The password to sign in with, if you need.')
    args = parser.parse_args()

    github = Github(args.username, args.password)

    repos = open("repo_info.csv", "r")
    for item in repos.readlines():
        print('Retreiving issue data from ' + item )
        print("item : " + item)
        repo_name = item.split(",")[1].rstrip()
        print(repo_name)
        summary = get_issues(repo_name)
        print("summary: ", summary)
