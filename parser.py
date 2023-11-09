import json
import sys
from string import Template

# 0  full_name
# 1  updated_at
# 2  pushed_at
# 3  default_branch
# 4  archived
# 5  disabled
# 6  tag_name
# 7  published_time
# 8  commit sha
# 9  commit time
# 10 message
T = "{0: <30}| {1: <25}| {2: <25}| {3: <20}| {4: <10}| {5: <10}| {6: <20}| {7: <25}| {8: <10}| {9: <25}| {10}"


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


def load_template():
    with open("row.html", "r") as f:
        return Template(f.read())


def build_str():
    t = load_template()
    n = sys.argv[1]
    rep = load_repo()
    rel = load_release()
    com = load_commit()
    if 'message' in rep:
        return t.substitute(
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
        return t.substitute(
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


def main():
    print(build_str())


if __name__ == '__main__':
    main()
