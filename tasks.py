import os

import jinja2
import requests
from dotenv import load_dotenv

load_dotenv()
DOMAIN = os.getenv("MAILGUN_DOMAIN")

template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)


def render_template(template, **context):
    return template_env.get_template(template).render(**context)


def send_simple_message(to, subject, body, html):
    key = os.getenv("MAILGUN_KEY")
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", key),
        data={
            "from": f"Excited User <mailgun@{DOMAIN}>",
            "to": [to],
            "subject": subject,
            "text": body,
            "html": html,
        },
    )


def send_registration_email(email, username):
    return send_simple_message(
        email,
        "Successfully signed up",
        f"Hi {username}, Welcome to the app",
        render_template("email/action.html", username=username),
    )
