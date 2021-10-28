from datetime import timedelta

from django.utils import timezone

from .models import ViewTrack


def cleanup_old_view_tracks(days=None):
    if days is None:
        raise Exception("cleanup_old_view_tracks must specify days")

    return ViewTrack.objects.filter(
        timestamp__lt=timezone.now() - timedelta(days=days)
    ).delete()[0]
