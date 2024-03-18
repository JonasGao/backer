import mail
from report.render import render_report
from report.repo import load_repos, load_latest, save_latest


def filter_diff(repos):
    has = 0
    has_diff_repo = []
    for p in repos:
        if p.has_change():
            has = has + 1
            has_diff_repo.append(p.name)
    return has, has_diff_repo


def main():
    suc, msg, repos = load_repos()
    if not suc:
        print("load_repos:", msg)
        return
    suc, msg, latest = load_latest()
    if suc:
        for p in repos:
            old = latest.get(p.full_name)
            if old is not None:
                p.diff(old)
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
    save_latest(repos)


if __name__ == '__main__':
    main()
