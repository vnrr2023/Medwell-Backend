from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Template
import os

conf = ConnectionConfig(
    MAIL_USERNAME=os.environ["MAIL_USERNAME"],
    MAIL_PASSWORD=os.environ["MAIL_PASSWORD"],
    MAIL_FROM=os.environ["MAIL_FROM"],
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)

def render_template(template_name: str, **kwargs):
    with open(template_name, "r", encoding="utf-8") as file:
        template = Template(file.read())
    return template.render(**kwargs)

def send_mail(first_name:str,email:str,pdf_name:str,status:str):
    container_class = "container-success" if status.lower() == "Success" else "container-failed"
    html_content = render_template(
            "send.html",
            user_name=first_name,
            pdf_name=pdf_name,
            status_message=status,
            container_class=container_class
        )

    message = MessageSchema(
            subject="Medwell Report Processing Status",
            recipients=[email],
            body=html_content,
            subtype="html"
        )

    fm = FastMail(conf)
    fm.send_message(message)
