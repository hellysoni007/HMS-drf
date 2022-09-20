from celery import shared_task
from hms import settings
from django.core.mail import send_mail


@shared_task
def email_service(to, subject, body):
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        to,
        fail_silently=False,
    )
    return "Done"
