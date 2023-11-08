import json
import sys


def main():
    n = sys.argv[1]
    s = ""
    ud = "Unknown"
    pd = "Unknown"
    db = "Unknown"
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
    print("{0: <30}| {1: <25}| {2: <25}| {3: <20}| {4}".format(n, ud, pd, db, m))


if __name__ == '__main__':
    main()
