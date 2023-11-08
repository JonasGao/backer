import json
import sys


def main():
    n = sys.argv[1]
    s = ""
    ud = "?"
    pd = "?"
    db = "?"
    ds = "?"
    ac = "?"
    for line in sys.stdin:
        if line.startswith("gh:"):
            break
        s += line
    d = json.loads(s)
    if 'message' in d:
        m = "⚠️ " + d['message']
    else:
        m = "None"
        n = d['full_name']
        ud = d['updated_at']
        pd = d['pushed_at']
        db = d['default_branch']
        ds = d['disabled']
        ac = d['archived']
    print("{0: <30}| {1: <25}| {2: <25}| {3: <20}| {4: <6}| {5: <6}| {6}"
          .format(n, ud, pd, db, ac, ds, m))


if __name__ == '__main__':
    main()
