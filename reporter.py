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
        repo['tag_name'] = re["name"] if r else ""
        repo['tag_published_at'] = re["published_at"] if r else ""
        repo['changed'] = False


def load_latest():
    if not os.path.isfile('latest_report.txt'):
        return False, "Not found latest_report.txt", dict()
    try:
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
    except Exception as e:
        print(e)
        return False, "Failed load latest_report.txt", dict()


def diff(repo, old):
    repo['pushed_at_changed'] = repo['pushed_at'] != old['pushed_at']
    repo['default_branch_changed'] = repo['default_branch'] != old['default_branch']
    repo['archived_changed'] = repo['archived'] != old['archived']
    repo['disabled_changed'] = repo['disabled'] != old['disabled']
    repo['tag_name_changed'] = repo['tag_name'] != old['tag_name']
    repo['tag_published_at_changed'] = repo['tag_published_at'] != old['tag_published_at']
    repo['commit_sha_changed'] = repo['commit_sha'] != old['commit_sha']


def has_diff(repos):
    has = 0
    for repo in repos:
        if repo['pushed_at_changed'] or \
                repo['default_branch_changed'] or \
                repo['archived_changed'] or \
                repo['disabled_changed'] or \
                repo['tag_name_changed'] or \
                repo['tag_published_at_changed'] or \
                repo['commit_sha_changed']:
            repo['changed'] = True
            has = has + 1
    return has


def save_latest(txt):
    with open("report.txt", "a") as f:
        f.write(txt)


def render_report(repos):
    ht = load_template("row.html")
    ca = []
    ha = []
    for repo in repos:
        if repo['changed']:
            ca.append(ht.render(repo))
        else:
            ha.append(ht.render(repo))
    bt = load_template("table.html")
    html = bt.render(dict(change=''.join(ca), other=''.join(ha)))
    return html


def render_latest(repos):
    t = load_template("row.txt")
    a = []
    for repo in repos:
        a.append(t.render(repo))
    return '\n'.join(a)


def main():
    suc, msg, repos = load_repos()
    if not suc:
        print("load_repos:", msg)
        return
    fetch_repos(repos)
    suc, msg, latest = load_latest()
    if suc:
        for repo in repos:
            old = latest[repo['full_name']]
            diff(repo, old)
        d = has_diff(repos)
        if d > 0:
            mail.send("发现有{0}个仓库更新".format(d), render_report(repos))
        else:
            print("No diff, skip report.")
    else:
        print("load_latest:", msg)
        mail.send("未找到上一次的记录，以下是当前仓库信息", render_report(repos))
    save_latest(render_latest(repos))


if __name__ == '__main__':
    main()
