import json
import sys

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


def main():
    n = sys.argv[1]
    rep = load_repo()
    rel = load_release()
    com = load_commit()
    if 'message' in rep:
        print(T.format(
            n,  # 0
            '?',  # 1
            '?',  # 2
            '?',  # 3
            '?',  # 4
            '?',  # 5
            '?',  # 6
            '?',  # 7
            '?',  # 8
            '?',  # 9
            "⚠️ " + rep['message']
        ))
    else:
        print(T.format(
            rep['full_name'],  # 0
            rep['updated_at'],  # 1
            rep['pushed_at'],  # 2
            rep['default_branch'],  # 3
            rep['archived'],  # 4
            rep['disabled'],  # 5
            rel["name"],  # 6
            rel["publishedAt"],  # 7
            com["sha"][0:8],  # 8
            com["commit"]["committer"]["date"],  # 9
            ""  # 10
        ))


if __name__ == '__main__':
    main()
