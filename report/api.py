import http.client
import json
import os
from dataclasses import dataclass

TOKEN = "Bearer " + os.getenv("GITHUB_TOKEN", "")


@dataclass
class Repo:
    owner: str
    repo: str
    full_name: str
    changed = False
    # Load from repo api
    disabled = False
    archived = False
    default_branch: str = None
    pushed_at: str = None
    updated_at: str = None
    name: str = None
    # Load from commit api
    commit_branch: str = None
    commit_msg: str = None
    commit_at: str = None
    commit_sha: str = None
    # Load from tag api
    tag_published_at: str = None
    tag_name: str = None
    # After Diff
    commit_sha_changed: bool = False
    tag_published_at_changed: bool = False
    tag_name_changed: bool = False
    disabled_changed: bool = False
    archived_changed: bool = False
    default_branch_changed: bool = False
    pushed_at_changed: bool = False

    def load_base(self):
        r, b = get(f"/repos/{self.owner}/{self.repo}")
        r, d = read(r, b)
        if r:
            self.name = d.get('name')
            self.full_name = d.get('full_name')
            self.updated_at = d.get('updated_at')
            self.pushed_at = d.get('pushed_at')
            self.default_branch = d.get('default_branch')
            self.archived = d.get('archived')
            self.disabled = d.get('disabled')
        return r

    def load_commit(self):
        r, cm = get_commit(self.owner, self.repo)
        if r:
            self.commit_sha = cm.get("sha")
            self.commit_at = cm["commit"]["committer"]["date"]
            self.commit_msg = cm["commit"]["message"]
            r, bs = get_branch_where_head(self.owner, self.repo, cm['sha'])
            if r:
                ab = []
                for br in bs:
                    ab.append(br['name'])
                self.commit_branch = ','.join(ab)
        return r

    def load_tag(self):
        r, re = get_release(self.owner, self.repo)
        if r:
            self.tag_name = re["name"]
            self.tag_published_at = re["published_at"]
        return r

    def load_more(self):
        self.load_base()
        self.load_commit()
        self.load_tag()

    def diff(self, old):
        self.pushed_at_changed = self.pushed_at != old['pushed_at']
        self.default_branch_changed = self.default_branch != old['default_branch']
        self.archived_changed = self.archived != old['archived']
        self.disabled_changed = self.disabled != old['disabled']
        self.tag_name_changed = self.tag_name != old['tag_name']
        self.tag_published_at_changed = self.tag_published_at != old['tag_published_at']
        self.commit_sha_changed = self.commit_sha != old['commit_sha']

    def has_diff(self):
        # return repo['pushed_at_changed'] or \
        return self.default_branch_changed or \
            self.archived_changed or \
            self.disabled_changed
        # repo['tag_name_changed'] or \
        # repo['tag_published_at_changed'] or \
        # repo['commit_sha_changed']

    def to_dict(self):
        return dict(
            owner=self.owner,
            repo=self.repo,
            full_name=self.full_name,
            changed=self.changed,
            disabled=self.disabled,
            archived=self.archived,
            default_branch=self.default_branch,
            pushed_at=self.pushed_at,
            updated_at=self.updated_at,
            name=self.name,
            commit_branch=self.commit_branch,
            commit_msg=self.commit_msg,
            commit_at=self.commit_at,
            commit_sha=self.commit_sha,
            tag_published_at=self.tag_published_at,
            tag_name=self.tag_name,
            commit_sha_changed=self.commit_sha_changed,
            tag_published_at_changed=self.tag_published_at_changed,
            tag_name_changed=self.tag_name_changed,
            disabled_changed=self.disabled_changed,
            archived_changed=self.archived_changed,
            default_branch_changed=self.default_branch_changed,
            pushed_at_changed=self.pushed_at_changed,
        )


def create_repo_from_csv(row):
    repo = Repo(owner=row[0], repo=row[1], full_name=row[0] + '/' + row[1])
    repo.load_more()
    return repo


def create_repo_from_latest(row):
    repo = Repo(owner="", repo="", full_name=row[0])
    repo.updated_at = row[1]
    repo.pushed_at = row[2]
    repo.default_branch = row[3]
    repo.tag_name = row[6]
    repo.tag_published_at = row[7]
    repo.commit_sha = row[8]
    repo.commit_at = row[9]
    repo.commit_msg = row[10]
    repo.archived = (row[4] == 'True'),
    repo.disabled = (row[5] == 'True')
    return repo


def get(url):
    conn = http.client.HTTPSConnection("api.github.com")
    conn.request("GET", url, None, {
        "User-Agent": "Backer/0.1 python3",
        "Authorization": TOKEN,
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
        return r, None


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
    # print(get_repo("Watfaq", "clash-rs"))
    print(get_commit("Watfaq", "clash-rs"))
    print(get_branch_where_head("Watfaq", "clash-rs", "91a0ce534d93c14273b4802a128795ccb2154f77"))
    print(get_release("Watfaq", "clash-rs"))
