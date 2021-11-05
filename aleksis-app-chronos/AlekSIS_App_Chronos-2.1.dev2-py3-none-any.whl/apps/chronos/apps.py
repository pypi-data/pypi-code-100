from django.db import transaction

from reversion.signals import post_revision_commit

from aleksis.core.util.apps import AppConfig


class ChronosConfig(AppConfig):
    name = "aleksis.apps.chronos"
    verbose_name = "AlekSIS — Chronos (Timetables)"

    urls = {
        "Repository": "https://edugit.org/AlekSIS/official/AlekSIS-App-Chronos/",
    }
    licence = "EUPL-1.2+"
    copyright_info = (
        ([2018, 2019, 2020, 2021], "Jonathan Weth", "wethjo@katharineum.de"),
        ([2018, 2019], "Frank Poetzsch-Heffter", "p-h@katharineum.de"),
        ([2019, 2020], "Dominik George", "dominik.george@teckids.org"),
        ([2019, 2021], "Hangzhi Yu", "yuha@katharineum.de"),
        ([2019], "Julian Leucker", "leuckeju@katharineum.de"),
        ([2019], "Tom Teichler", "tom.teichler@teckids.org"),
        ([2021], "Lloyd Meins", "meinsll@katharineum.de"),
    )

    def ready(self):
        super().ready()

        from .util.change_tracker import handle_new_revision  # noqa

        def _handle_post_revision_commit(sender, revision, versions, **kwargs):
            """Handle a new post revision commit signal in background."""
            transaction.on_commit(lambda: handle_new_revision.delay(revision.pk))

        post_revision_commit.connect(_handle_post_revision_commit, weak=False)
