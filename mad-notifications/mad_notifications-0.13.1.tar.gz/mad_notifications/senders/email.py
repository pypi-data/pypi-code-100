import datetime
from django.conf import settings
from mad_notifications.settings import notification_settings
from django.template import Template, Context
from django.core.mail import send_mail
from django.conf import settings


class EmailNotification:
    
    def __init__(self, notification):
        self.notification = notification


    def emailNotification(self):
        notification_obj = self.notification

        # from email
        from_email = settings.DEFAULT_FROM_EMAIL
        if notification_obj.template.from_email is not None or notification_obj.template.from_email != "":
            from_email = notification_obj.template.from_email


        try:
            # templating of email content
            template = Template(notification_obj.template.content)
            context = Context(notification_obj.data)
            html_message = template.render(context)
        except Exception as e:
            html_message = None

        try:
            # send email
            sent = send_mail(
                subject = notification_obj.title,
                message = notification_obj.content,
                from_email = from_email,
                recipient_list = [notification_obj.user.email],
                fail_silently = False,
                html_message = html_message,
            )
            return sent
        except Exception as e:
            raise



def sendEmailNotification(notification):
    firebase_push_notification = notification_settings.EMAIL_NOTIFICATION_CLASS(notification)
    return firebase_push_notification.emailNotification()