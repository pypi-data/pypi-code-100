import unittest
from pathlib import Path

from ruteni import ROOTNS
from ruteni.plugins.pwa import Display, ProgressiveWebApp, RelatedApplication
from ruteni.utils.color import Color
from ruteni.utils.icon import PngIcon
from urlobject.path import URLPath


class ProgressiveWebAppTestCase(unittest.TestCase):
    def test_get_manifest(self) -> None:
        icons = [
            PngIcon(
                ROOTNS,
                URLPath(f"{size}x{size}.png"),
                Path(f"tests/icons/icon-{size}x{size}.png"),
            )
            for size in (72, 96, 120, 128, 144, 152, 180, 192, 384, 512)
        ]

        # with self.assertRaises(UnknownColor):
        pwa = ProgressiveWebApp(
            "app_name",
            1,
            display=Display.BROWSER,
            theme_color=Color("white"),
            background_color=Color("#ffffff"),
        )
        pwa.add_i18n(
            "en-US",
            full_name="full name",
            short_name="short name",
            description="description",
        )
        pwa.add_i18n(
            "fr-FR",
            full_name="nom entier",
            short_name="nom court",
            description="description",
        )

        for icon in icons:
            pwa.add_icon(icon)

        pwa.add_related_application(
            RelatedApplication(platform="play", id="com.google.samples.apps.iosched")
        )

        with self.assertRaises(KeyError):
            pwa.get_manifest("de-DE")

        self.assertEqual(
            pwa.get_manifest("en-US"),
            {
                "lang": "en-US",
                "icons": [
                    {"src": "/72x72.png", "sizes": "72x72", "type": "image/png"},
                    {"src": "/96x96.png", "sizes": "96x96", "type": "image/png"},
                    {"src": "/120x120.png", "sizes": "120x120", "type": "image/png"},
                    {"src": "/128x128.png", "sizes": "128x128", "type": "image/png"},
                    {"src": "/144x144.png", "sizes": "144x144", "type": "image/png"},
                    {"src": "/152x152.png", "sizes": "152x152", "type": "image/png"},
                    {"src": "/180x180.png", "sizes": "180x180", "type": "image/png"},
                    {"src": "/192x192.png", "sizes": "192x192", "type": "image/png"},
                    {"src": "/384x384.png", "sizes": "384x384", "type": "image/png"},
                    {"src": "/512x512.png", "sizes": "512x512", "type": "image/png"},
                ],
                "start_url": "/app/app_name/",
                "name": "full name",
                "short_name": "short name",
                "description": "description",
                "display": "browser",
                "theme_color": "white",
                "background_color": "#ffffff",
                "related_applications": [
                    {"platform": "play", "id": "com.google.samples.apps.iosched"}
                ],
            },
        )

        self.assertEqual(
            pwa.get_manifest("fr-FR"),
            {
                "lang": "fr-FR",
                "icons": [
                    {"src": "/72x72.png", "sizes": "72x72", "type": "image/png"},
                    {"src": "/96x96.png", "sizes": "96x96", "type": "image/png"},
                    {"src": "/120x120.png", "sizes": "120x120", "type": "image/png"},
                    {"src": "/128x128.png", "sizes": "128x128", "type": "image/png"},
                    {"src": "/144x144.png", "sizes": "144x144", "type": "image/png"},
                    {"src": "/152x152.png", "sizes": "152x152", "type": "image/png"},
                    {"src": "/180x180.png", "sizes": "180x180", "type": "image/png"},
                    {"src": "/192x192.png", "sizes": "192x192", "type": "image/png"},
                    {"src": "/384x384.png", "sizes": "384x384", "type": "image/png"},
                    {"src": "/512x512.png", "sizes": "512x512", "type": "image/png"},
                ],
                "start_url": "/app/app_name/",
                "name": "nom entier",
                "short_name": "nom court",
                "description": "description",
                "display": "browser",
                "theme_color": "white",
                "background_color": "#ffffff",
                "related_applications": [
                    {"platform": "play", "id": "com.google.samples.apps.iosched"}
                ],
            },
        )
