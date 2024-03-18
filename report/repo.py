import csv
import os
from dataclasses import dataclass
from api import get, read
from render import render_latest

LATEST_RECORDS_NAME = 'latest_data.txt'
RECORDS_NAME = "data.txt"
REPO_LIST = 'report/repos.txt'


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
    # After Diff
    disabled_changed: bool = False
    archived_changed: bool = False
    default_branch_changed: bool = False

    def load_base(self):
        success, resp_bytes = get(f"/repos/{self.owner}/{self.repo}")
        success, resp_data = read(success, resp_bytes)
        if success:
            self.name = resp_data.get('name')
            self.full_name = resp_data.get('full_name')
            self.updated_at = resp_data.get('updated_at')
            self.pushed_at = resp_data.get('pushed_at')
            self.default_branch = resp_data.get('default_branch')
            self.archived = resp_data.get('archived')
            self.disabled = resp_data.get('disabled')
        return success

    def diff(self, old):
        self.default_branch_changed = self.default_branch != old.default_branch
        self.archived_changed = self.archived != old.archived
        self.disabled_changed = self.disabled != old.disabled
        if self.default_branch_changed or \
                self.archived_changed or \
                self.disabled_changed:
            self.changed = True

    def has_change(self):
        return self.changed

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
            disabled_changed=self.disabled_changed,
            archived_changed=self.archived_changed,
            default_branch_changed=self.default_branch_changed,
        )

    def save_for_diff(self):
        return render_latest(self)


def create_repo_from_csv(row):
    p = Repo(owner=row[0], repo=row[1], full_name=row[0] + '/' + row[1])
    p.load_base()
    return p


def create_repo_from_latest(row):
    return create_repo_for_diff(row[0], (row[1] == 'True'), (row[2] == 'True'), row[3])


def create_repo_for_diff(full_name, archived, disabled, default_branch):
    p = Repo(owner="", repo="", full_name=full_name)
    p.archived = archived
    p.disabled = disabled
    p.default_branch = default_branch
    return p


def load_repos():
    if not os.path.isfile(REPO_LIST):
        return False, f"Can not found {REPO_LIST}", []
    with open(REPO_LIST) as f:
        repo_arr = []
        for row in csv.reader(f, delimiter=","):
            repo_arr.append(create_repo_from_csv(row))
        return True, "", repo_arr


def load_latest() -> tuple[bool, str, dict]:
    if not os.path.isfile(LATEST_RECORDS_NAME):
        return False, f"Not found '{LATEST_RECORDS_NAME}'", dict()
    try:
        with open(LATEST_RECORDS_NAME) as f:
            repo_dict = dict()
            for row in csv.reader(f, delimiter="|"):
                p = create_repo_from_latest(row)
                repo_dict[p.full_name] = p
            return True, "", repo_dict
    except Exception as e:
        print(e)
        return False, f"Failed load '{LATEST_RECORDS_NAME}'", dict()


def save_latest(repos):
    repo_string_lines = []
    for p in repos:
        repo_string_lines.append(p.save_for_diff())
    with open(RECORDS_NAME, "a") as f:
        f.write('\n'.join(repo_string_lines))


if __name__ == '__main__':
    a = Repo(owner="Watfaq", repo="clash-rs", full_name="Watfaq/clash-rs")
    a.load_base()
    b = create_repo_for_diff("Watfaq/clash-rs", False, False, "master")
    a.diff(b)
    print(a.changed)
    r, m, d = load_latest()
    print(d[a.full_name].changed)
