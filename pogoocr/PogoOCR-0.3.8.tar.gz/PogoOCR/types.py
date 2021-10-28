import datetime
import decimal
import json
import logging
import math
import os
import re
from io import BytesIO
from string import digits
from typing import Optional

import requests
from babel import Locale
from babel.numbers import get_group_symbol, NumberFormatError
from dateutil.parser import parse as parse_date
from PIL import Image as PILImage

from .cloudvision import Image
from .numbers import parse_decimal, parse_number

log: logging.Logger = logging.getLogger(__name__)

TEAMLESS = 0
MYSTIC = 1
VALOR = 2
INSTINCT = 3

TEAM_COLOURS = (
    (None, (0, 0, 0)),
    (None, (159, 228, 163)),  # Friends List Page
    (None, (160, 208, 150)),  # Badge Pages
    (TEAMLESS, (0.0, 231.0, 181.0)),
    (MYSTIC, (6.5, 118.8, 241.6)),
    (VALOR, (255.0, 4.0, 42.0)),
    (INSTINCT, (253.0, 202.0, 0.1)),
)


class ProfileSelf(Image):
    def __init__(self, service_file: str, image_uri: str) -> None:
        super().__init__(service_file, image_uri)
        self.pilimage = PILImage.open(BytesIO(requests.get(image_uri).content))
        self.pilimage = self.pilimage.convert(mode="RGB")
        self._team = None
        self.locale = Locale.parse("en")
        self.numeric_locale = {}
        with open(os.path.join(os.path.dirname(__file__), "pattern_lookups.json"), "r") as f:
            self.pattern_lookups = json.load(f)

    def get_text(self, force: Optional[bool] = False) -> None:
        # Check if an API call needs to be made.
        # Prevents accidental extra calls to a premium API
        if force or not hasattr(self, "text_found"):
            super().get_text()

        # Try to work out locale:
        locale_lookup = [
            (Locale.parse("fr"), r"(?:(?:Activit[ée]s\stotales)|(?:PROGR[ÈE]S\sDE\sLA\sSEMAINE))"),
            (
                Locale.parse("de"),
                r"(?:(?:Aktivit[äa]tsstatistik)|(?:W[ÖO]CHENTLICHER\sFORTSCHRITT))",
            ),
            (Locale.parse("it"), r"(?:(?:Riepilogo\sattivit[àa])|(?:PROGRESSI\sSETTIMANALI))"),
            (Locale.parse("ja"), r"(?:(?:アクティビティ)|(?:ウィークリー))"),
            (Locale.parse("ko"), r"(?:(?:활동)|(?:주간\s피트니스))"),
            (Locale.parse("es"), r"(?:(?:Total\sde\sactividades)|(?:PROGRESO\sSEMANAL))"),
            (Locale.parse("zh_hant"), r"(?:(?:活動紀錄)|(?:本週成果))"),
            (Locale.parse("en"), r"(?:(?:Total\sActivity)|(?:WEEKLY\sPROGRESS))"),
            (Locale.parse("pt_br"), r"(?:(?:Total\sde\satividades)|(?:PROGRESSO\sSEMANAL))"),
            (Locale.parse("th"), r"(?:(?:กิจกรรมทั้งหมด)|(?:ความคืบหน้าประจำสัปดาห์))"),
        ]
        for locale, pattern in locale_lookup:
            if re.search(pattern, self.text_found[0].description, re.IGNORECASE):
                self.locale = locale
                break

        # Since the only stat that is a decimal is travel_km, we will check that.
        try:
            travel_km = (
                re.search(
                    self.pattern_lookups[self.locale.language]["travel_km"] + "\s?[;:：]?\n(.+)",
                    self.text_found[0].description,
                    re.IGNORECASE,
                )[1]
                .replace("km", "")
                .strip()
                .replace(" ", "\xa0")
            )
        except (decimal.InvalidOperation, TypeError):
            pass
        else:
            translated = travel_km.translate(str.maketrans("", "", digits))
            self.numeric_locale["decimal"] = translated[-1]
            if len(translated) > 1:
                self.numeric_locale["group"] = translated[-2]

        # If travel_km wasn't big enough to get the group for numeric_locale, try total_xp
        if self.numeric_locale.get("group") is None:
            try:
                total_xp = (
                    re.search(
                        self.pattern_lookups[self.locale.language]["total_xp"] + "\s?[;:：]?\n(.+)",
                        self.text_found[0].description,
                        re.IGNORECASE,
                    )[1]
                    .strip()
                    .replace(" ", "\xa0")
                )
            except (ValueError, TypeError):
                # Assume Locale
                self.numeric_locale["group"] = get_group_symbol(self.locale)
            else:
                translated = total_xp.translate(str.maketrans("", "", digits))
                self.numeric_locale["group"] = translated[0]

    def _calculate_colour_distance(self, c1, c2):
        (r1, g1, b1) = c1
        (r2, g2, b2) = c2
        return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

    def get_team(self) -> int:
        # Get the pixel in the middle, 2 pixels in
        # This is because the game adds borders to your profile to match your team colour
        pixel_location = (2, self.pilimage.size[1] / 2)
        rgb = self.pilimage.getpixel(pixel_location)
        closest_colours = sorted(
            TEAM_COLOURS, key=lambda colour: self._calculate_colour_distance(colour[1], rgb)
        )
        log.debug(f"RGB: {rgb}")
        log.debug(f"Guesses: {closest_colours}")
        best_guess = closest_colours[0][0]
        return best_guess

    @property
    def username(self) -> Optional[str]:
        try:
            return re.search(
                r"([A-Za-z0-9]+)\n(?:\&|et|con|e) ?(.+)", self.text_found[0].description
            )[1]
        except TypeError:
            log.exception("username failed to return")
            return None

    @property
    def buddy_name(self) -> Optional[str]:
        try:
            return re.search(
                r"([A-Za-z0-9]+)\n(?:\&|et|con|e) ?(.+)", self.text_found[0].description
            )[2]
        except TypeError:
            log.exception("buddy_name failed to return")
            return None

    @property
    def team(self) -> Optional[int]:
        if isinstance(self._team, int):
            return self._team
        else:
            self._team = self.get_team()
            return self._team

    @property
    def travel_km(self) -> Optional[decimal.Decimal]:
        try:
            result = (
                re.search(
                    self.pattern_lookups[self.locale.language]["travel_km"] + "\s?[;:：]?\n(.+)",
                    self.text_found[0].description,
                    re.IGNORECASE,
                )[1]
                .replace("km", "")
                .strip()
            )
            return parse_decimal(result, locale=self.numeric_locale)
        except (NumberFormatError, TypeError):
            log.exception("travel_km failed to return")
            return None

    @property
    def capture_total(self) -> Optional[int]:
        try:
            result = re.search(
                self.pattern_lookups[self.locale.language]["capture_total"] + "\s?[;:：]?\n(.+)",
                self.text_found[0].description,
                re.IGNORECASE,
            )[1].strip()
            return parse_number(result, locale=self.numeric_locale)
        except (NumberFormatError, TypeError):
            log.exception("capture_total failed to return")
            return None

    @property
    def pokestops_visited(self) -> Optional[int]:
        try:
            result = re.search(
                self.pattern_lookups[self.locale.language]["pokestops_visited"]
                + "\s?[;:：]?\n(.+)",
                self.text_found[0].description,
                re.IGNORECASE,
            )[1].strip()
            return parse_number(result, locale=self.numeric_locale)
        except (NumberFormatError, TypeError):
            log.exception("pokestops_visited failed to return")
            return None

    @property
    def total_xp(self) -> Optional[int]:
        try:
            result = re.search(
                self.pattern_lookups[self.locale.language]["total_xp"] + "\s?[;:：]?\n(.+)",
                self.text_found[0].description,
                re.IGNORECASE,
            )[1].strip()
            return parse_number(result, locale=self.numeric_locale)
        except (NumberFormatError, TypeError):
            log.exception("total_xp failed to return")
            return None

    @property
    def start_date(self) -> Optional[datetime.date]:
        try:
            result = re.search(
                self.pattern_lookups[self.locale.language]["start_date"] + "\s?[;:：]?\n(.+)",
                self.text_found[0].description,
                re.IGNORECASE,
            )[1]
            return parse_date(result).date()
        except (ValueError, OverflowError, TypeError):
            log.exception("start_date failed to return")
            return None

    def find_stats(self):
        return self.get_text(force=False)
