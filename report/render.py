from jinja2 import Environment, Template

TEMPLATE_PATH_RECORD = "report/row.txt"
TEMPLATE_PATH_TABLE = "report/table.html"
TEMPLATE_PATH_ROW = "report/row.html"
REPO_LIST = 'report/repos.txt'
env = Environment()
templates = dict()


def load_template(name) -> Template:
    if name in templates:
        return templates[name]
    with open(name, "r") as f:
        template = env.from_string(f.read())
        templates[name] = template
        return template


def render_latest(repo):
    return load_template(TEMPLATE_PATH_RECORD).render(repo.to_dict())


def render_report(repos):
    row_template = load_template(TEMPLATE_PATH_ROW)
    changed_arr = []
    for repo in repos:
        if repo.changed:
            changed_arr.append(row_template.render(repo.to_dict()))
    html_table = load_template(TEMPLATE_PATH_TABLE)
    html = html_table.render(dict(change=''.join(changed_arr)))
    return html
