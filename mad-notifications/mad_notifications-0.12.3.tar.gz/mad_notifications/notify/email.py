from django.template import Template, Context
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
import logging
from mad_notifications.models import Notification

logger = logging.getLogger(__name__)

@shared_task(name="Non-Periodic: Email notification")
def email_notification(notification_id):
    try:
        notification_obj = Notification.objects.get(id=notification_id)

        from_email = settings.DEFAULT_FROM_EMAIL
        if notification_obj.template.from_email is not None or notification_obj.template.from_email != "":
            from_email = notification_obj.template.from_email

        try:
            # templating of email content
            template = Template(notification_obj.template.content)
            context = Context(notification_obj.data)
            html_message = template.render(context)

            # send email
            send_mail(
                subject = notification_obj.title,
                message = notification_obj.content,
                from_email = from_email,
                recipient_list = [notification_obj.user.email],
                fail_silently = False,
                html_message = html_message,
            )

        except Exception as e:
            # send email
            send_mail(
                subject = notification_obj.title,
                message = notification_obj.content,
                from_email = from_email,
                recipient_list = [notification_obj.user.email],
                fail_silently = False,
            )

        return "Email notifications sent"

    except Exception as e:
        logger.warning(str(e))
        return "Unable to send Email notification: " + str(e)
