from django.template.loader import render_to_string
from datetime import datetime

def create_html(email,pdf_name,status):
    container_class = 'container-success' if status=="SUCCESS" else 'container-failed'
    status_message = 'Success' if status=="SUCCESS" else 'Failed'

    # Render HTML template with context
    html_content = render_to_string('report_status_email.html', {
        'user_name': email,
        'pdf_name': pdf_name,
       'container_class': container_class,
        'status_message': status_message,
    })
    return html_content