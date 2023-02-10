from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import time


# @shared_task
# def timesleep():
#     print("timesleep")
@shared_task
def sendemail():
    subject = "welcome to Elearning course"
    message = f"Hi Thank you for registering in Elearning ."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['hegdeshashu1@gmail.com']
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    print("Mail sent")

    