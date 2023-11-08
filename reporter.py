import http.client
import json


def get_repo(owner, repo):
    conn = http.client.HTTPSConnection("api.github.com")
    conn.request("GET", f"/repos/{owner}/{repo}", None,
                 {"User-Agent": "Backer/0.1 python3"})
    r = conn.getresponse()
    print(r.status, r.reason)
    if r.status == 200:
        d = r.read()
        print(d)
        d = json.loads(d)
    else:
        d = r.read()
        d = repr(d)
    conn.close()
    return d


def main():
    repo = get_repo("Watfaq", "clash-rs")
    print(repo)


if __name__ == '__main__':
    main()
