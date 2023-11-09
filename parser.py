import csv
import json
import os.path
import sys

from jinja2 import Environment

env = Environment()


def load_json(name):
    with open(name, "r") as f:
        fd = f.read()
        d = json.loads(fd)
        return d


def load_template(name):
    with open(name, "r") as f:
        return env.from_string(f.read())


def load_latest(name):
    if not os.path.isfile('latest_report.txt'):
        return None
    with open('latest_report.txt') as f:
        s = csv.reader(f, delimiter="|")
        for row in s:
            if row[0] == name:
                return row


def chk_val(v1, latest, index):
    if not latest:
        return dict(value=v1, changed=False)
    v2 = latest[index]
    if str(v1) == v2:
        return dict(value=v1, changed=False)
    else:
        return dict(value=v1, changed=True)


def build_str():
    n = sys.argv[1]
    ht = load_template("row.html")
    tt = load_template("row.txt")
    rep = load_json("repo.txt")
    rel = load_json("rele.txt")
    com = load_json("lcom.txt")[0]
    lat = load_latest(n)
    unk = dict(value='?', changed=False)
    if 'message' in rep:
        d = dict(
            full_name=n,
            updated_at='?',
            pushed_at=unk,
            default_branch=unk,
            archived=unk,
            disabled=unk,
            tag_name=unk,
            tag_publishedAt='?',
            commit_sha=unk,
            commit_at='?',
            message="⚠️ " + rep['message'],
        )
    else:
        d = dict(
            full_name=rep['full_name'],
            updated_at=rep['updated_at'],
            pushed_at=chk_val(rep['pushed_at'], lat, 2),
            default_branch=chk_val(rep['default_branch'], lat, 3),
            archived=chk_val(rep['archived'], lat, 4),
            disabled=chk_val(rep['disabled'], lat, 5),
            tag_name=chk_val(rel["name"], lat, 6),
            tag_publishedAt=rel["publishedAt"],
            commit_sha=chk_val(com["sha"][0:8], lat, 8),
            commit_at=com["commit"]["committer"]["date"],
            message="",
        )
    return dict(
        html=ht.render(d),
        txt=tt.render(d),
    )


def main():
    d = build_str()
    with open("report.html", "a") as f:
        f.write(d['html'])
    with open("report.txt", "a") as f:
        f.write(d['txt'])


if __name__ == '__main__':
    main()
