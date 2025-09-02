from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path


def render_weekly_report(context: dict) -> str:
    base = Path(__file__).resolve().parents[1] / "templates" / "report"
    env = Environment(
        loader=FileSystemLoader(str(base)),
        autoescape=select_autoescape(['html'])
    )
    # Nota: Template scritto stile Handlebars, ma Jinja supporta {{ }} e {% for %}.
    template = env.get_template("weekly_report.html.hbs")
    return template.render(**context)

