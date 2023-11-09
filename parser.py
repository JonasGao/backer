import json
import sys
from string import Template


def load_repo():
    with open("repo.txt", "r") as f:
        fd = f.read()
        d = json.loads(fd)
        return d


def load_release():
    with open("rele.txt", "r") as f:
        fd = f.read()
        d = json.loads(fd)
        return d


def load_commit():
    with open("lcom.txt", "r") as f:
        fd = f.read()
        d = json.loads(fd)
        return d[0]


def load_html_template():
    with open("row.html", "r") as f:
        return Template(f.read())


def load_txt_template():
    with open("row.txt", "r") as f:
        return Template(f.read())


def build_str():
    ht = load_html_template()
    tt = load_txt_template()
    n = sys.argv[1]
    rep = load_repo()
    rel = load_release()
    com = load_commit()
    if 'message' in rep:
        d = dict(
            full_name=n,
            updated_at='?',
            pushed_at='?',
            default_branch='?',
            archived='?',
            disabled='?',
            tag_name='?',
            tag_publishedAt='?',
            commit_sha='?',
            commit_at='?',
            message="⚠️ " + rep['message'],
        )
    else:
        d = dict(
            full_name=rep['full_name'],
            updated_at=rep['updated_at'],
            pushed_at=rep['pushed_at'],
            default_branch=rep['default_branch'],
            archived=rep['archived'],
            disabled=rep['disabled'],
            tag_name=rel["name"],
            tag_publishedAt=rel["publishedAt"],
            commit_sha=com["sha"][0:8],
            commit_at=com["commit"]["committer"]["date"],
            message=com["commit"]["message"],
        )
    return dict(
        html=ht.substitute(d),
        txt=tt.substitute(d),
    )


def main():
    d = build_str()
    with open("report.html", "a") as f:
        f.write(d['html'])
    with open("report.txt", "a") as f:
        f.write(d['txt'])


if __name__ == '__main__':
    main()
