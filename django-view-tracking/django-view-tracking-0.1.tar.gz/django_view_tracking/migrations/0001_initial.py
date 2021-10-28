from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ViewTrack",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("request_method", models.CharField(max_length=7)),
                (
                    "request_url",
                    models.TextField(
                        validators=[django.core.validators.URLValidator()]
                    ),
                ),
                ("response_status_code", models.PositiveSmallIntegerField()),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="view_tracks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
