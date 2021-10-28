import datetime
from django.conf import settings
from firebase_admin import credentials, messaging
from google.oauth2 import service_account
from mad_notifications.settings import notification_settings
from mad_notifications.models import Notification

from celery import shared_task

import json
import firebase_admin


class FirebaseMobilePushNotification:
    
    def __init__(self, device, notification):
        self.device = device
        self.notification = notification


    def mobilePushNotification(self):
        device = self.device
        notification_obj = self.notification

        message = messaging.Message(
            token=device.token,
            notification=messaging.Notification(
                title=notification_obj.title,
                body=notification_obj.content,
                image=notification_obj.image.url if notification_obj.image else '' ,
            ),
            android=messaging.AndroidConfig(
                ttl=datetime.timedelta(seconds=3600),
                priority='high',
                notification=messaging.AndroidNotification(
                    icon=notification_obj.icon.url if notification_obj.icon else '' ,
                    default_sound=True,
                    sound='default',
                    color='#ffffff',
                    default_light_settings=True
                )
            ),
            apns=messaging.APNSConfig(
                headers={'apns-priority': '10'},
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        sound=messaging.CriticalSound (
                            name="default",
                            volume=1.0
                        )
                    ),
                ),
            ),
            data=notification_obj.data
        )
        return messaging.send(message)



def sendFirebaseMobilePushNotification(device, notification):
    firebase_push_notification = notification_settings.FIREBASE_MOBILE_PUSH_NOTIFICATION_CLASS(device, notification)
    return firebase_push_notification.mobilePushNotification()