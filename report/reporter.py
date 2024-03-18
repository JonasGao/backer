import csv
import os

import api
from jinja2 import Environment

import mail

TEMPLATE_RECORD = "report/row.txt"
TEMPLATE_TABLE = "report/table.html"
TEMPLATE_ROW = "report/row.html"
REPO_LIST = 'report/repos.txt'
env = Environment()


def load_template(name):
    with open(name, "r") as f:
        return env.from_string(f.read())


def load_repos():
    if not os.path.isfile(REPO_LIST):
        return False, f"Can not found {REPO_LIST}", []
    with open(REPO_LIST) as f:
        a = []
        for row in csv.reader(f, delimiter=","):
            a.append(api.create_repo_from_csv(row))
        return True, "", a


def load_latest():
    if not os.path.isfile('latest_report.txt'):
        return False, "Not found latest_report.txt", dict()
    try:
        with open('latest_report.txt') as f:
            a = dict()
            for row in csv.reader(f, delimiter="|"):
                repo = api.create_repo_from_latest(row)
                a[repo.full_name] = repo
            return True, "", a
    except Exception as e:
        print(e)
        return False, "Failed load latest_report.txt", dict()


def filter_diff(repos):
    has = 0
    has_diff_repo = []
    for repo in repos:
        if repo.has_diff():
            repo.changed = True
            has = has + 1
            has_diff_repo.append(repo.name)
    return has, has_diff_repo


def save_latest(txt):
    with open("report.txt", "a") as f:
        f.write(txt)


def render_report(repos):
    ht = load_template(TEMPLATE_ROW)
    ca = []
    ha = []
    for repo in repos:
        if repo['changed']:
            ca.append(ht.render(repo))
        else:
            ha.append(ht.render(repo))
    bt = load_template(TEMPLATE_TABLE)
    html = bt.render(dict(change=''.join(ca), other=''.join(ha)))
    return html


def render_latest(repos):
    t = load_template(TEMPLATE_RECORD)
    a = []
    for repo in repos:
        a.append(t.render(repo))
    return '\n'.join(a)


def main():
    suc, msg, repos = load_repos()
    if not suc:
        print("load_repos:", msg)
        return
    suc, msg, latest = load_latest()
    if suc:
        for repo in repos:
            old = latest.get(repo.full_name)
            if old is not None:
                repo.diff(old)
        d, r = filter_diff(repos)
        if d <= 0:
            print("No diff, skip report.")
        elif d == 1:
            mail.send("{0} 更新".format(r[0]), render_report(repos))
        elif d == 2:
            mail.send("{0},{1} 更新".format(r[0], r[1]), render_report(repos))
        elif d == 3:
            mail.send("{0},{1},{2} 更新".format(r[0], r[1], r[2]), render_report(repos))
        else:
            mail.send("发现有{0}个仓库更新".format(d), render_report(repos))
    else:
        print("load_latest:", msg)
        mail.send("未找到上一次的记录，以下是当前仓库信息", render_report(repos))
    save_latest(render_latest(repos))


if __name__ == '__main__':
    main()
