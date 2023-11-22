import http.client
import json


def get(url):
    conn = http.client.HTTPSConnection("api.github.com")
    conn.request("GET", url, None, {
        "User-Agent": "Backer/0.1 python3",
        "Accept": "application/vnd.github+json"})
    r = conn.getresponse()
    print("Called get:", url, "Return:", r.status, r.reason)
    b = r.read()
    conn.close()
    return r.status == 200, b


def read(r, b):
    if r:
        d = json.loads(b)
        return r, d
    else:
        print("Read error response:", repr(b))
        return r


def get_repo(owner, repo):
    r, b = get(f"/repos/{owner}/{repo}")
    r, d = read(r, b)
    return r, d


# gh api "repos/$line/commits" > lcom.txt
def get_commit(owner, repo):
    r, b = get(f"/repos/{owner}/{repo}/commits?per_page=1&page=1")
    r, d = read(r, b)
    if r:
        return r, d[0]
    else:
        return r, d


# https://api.github.com/repos/OWNER/REPO/commits/COMMIT_SHA/branches-where-head
def get_branch_where_head(owner, repo, sha):
    r, b = get(f"/repos/{owner}/{repo}/commits/{sha}/branches-where-head")
    r, d = read(r, b)
    return r, d


# gh release view --repo "$line" --json name,publishedAt > rele.txt
# https://api.github.com/repos/OWNER/REPO/releases/latest
def get_release(owner, repo):
    r, b = get(f"/repos/{owner}/{repo}/releases/latest")
    r, d = read(r, b)
    return r, d


if __name__ == '__main__':
    print(get_repo("Watfaq", "clash-rs"))
    print(get_commit("Watfaq", "clash-rs"))
    print(get_branch_where_head("Watfaq", "clash-rs", "91a0ce534d93c14273b4802a128795ccb2154f77"))
    print(get_release("Watfaq", "clash-rs"))
