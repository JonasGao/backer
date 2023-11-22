import csv
import os

import api
from jinja2 import Environment

import mail

env = Environment()


def load_template(name):
    with open(name, "r") as f:
        return env.from_string(f.read())


def load_repos():
    if not os.path.isfile('repos.txt'):
        return False, "There is no repos.txt"
    with open('repos.txt') as f:
        a = []
        for row in csv.reader(f, delimiter=","):
            a.append(dict(owner=row[0], repo=row[1], full_name=row[0] + '/' + row[1]))
        return True, "", a


def fetch_repos(repos):
    for repo in repos:
        r, po = api.get_repo(repo['owner'], repo['repo'])
        if r:
            repo['full_name'] = po['full_name']
            repo['updated_at'] = po['updated_at']
            repo['pushed_at'] = po['pushed_at']
            repo['default_branch'] = po['default_branch']
            repo['archived'] = po['archived']
            repo['disabled'] = po['disabled']
        r, cm = api.get_commit(repo['owner'], repo['repo'])
        if r:
            repo['commit_sha'] = cm["sha"]
            repo['commit_at'] = cm["commit"]["committer"]["date"]
            repo['commit_msg'] = cm["commit"]["message"]
        r, bs = api.get_branch_where_head(repo['owner'], repo['repo'], cm['sha'])
        if r:
            ab = []
            for br in bs:
                ab.append(br['name'])
            repo['commit_branch'] = ','.join(ab)
        r, re = api.get_release(repo['owner'], repo['repo'])
        if r:
            repo['tag_name'] = re["name"]
            repo['tag_published_at'] = re["published_at"]


def load_latest():
    if not os.path.isfile('latest_report.txt'):
        return False, "Not found latest_report.txt", None
    with open('latest_report.txt') as f:
        a = dict()
        for row in csv.reader(f, delimiter="|"):
            a[row[0]] = dict(
                full_name=row[0],
                updated_at=row[1],
                pushed_at=row[2],
                default_branch=row[3],
                archived=(row[4] == 'True'),
                disabled=(row[5] == 'True'),
                tag_name=row[6],
                tag_published_at=row[7],
                commit_sha=row[8],
                commit_at=row[9],
                commit_msg=row[10],
            )
        return True, "", a


def diff(repo, old):
    repo['pushed_at_changed'] = repo['pushed_at'] != old['pushed_at']
    repo['default_branch_changed'] = repo['default_branch'] != old['default_branch']
    repo['archived_changed'] = repo['archived'] != old['archived']
    repo['disabled_changed'] = repo['disabled'] != old['disabled']
    repo['tag_name_changed'] = repo['tag_name'] != old['tag_name']
    repo['tag_published_at_changed'] = repo['tag_published_at'] != old['tag_published_at']
    repo['commit_sha_changed'] = repo['commit_sha'] != old['commit_sha']


def render(repos):
    ht = load_template("row.html")
    tt = load_template("row.txt")
    ha = []
    ta = []
    for repo in repos:
        ha.append(ht.render(repo))
        ta.append(tt.render(repo))
    ht = load_template("table.html")
    html = ht.render(dict(body=''.join(ha)))
    return html, '\n'.join(ta)


def has_diff(repos):
    for repo in repos:
        if repo['pushed_at_changed'] or \
                repo['default_branch_changed'] or \
                repo['archived_changed'] or \
                repo['disabled_changed'] or \
                repo['tag_name_changed'] or \
                repo['tag_published_at_changed'] or \
                repo['commit_sha_changed']:
            return True
    return False


def save_latest(txt):
    with open("report.txt", "a") as f:
        f.write(txt)


def main():
    suc, msg, repos = load_repos()
    if not suc:
        print("load_repos:", msg)
        return
    suc, msg, latest = load_latest()
    if not suc:
        print("load_latest:", msg)
        return
    fetch_repos(repos)
    for repo in repos:
        old = latest[repo['full_name']]
        diff(repo, old)
    if has_diff(repos):
        html, txt = render(repos)
        mail.send(html)
        save_latest(txt)
    else:
        print("No diff, skip report.")


if __name__ == '__main__':
    main()
