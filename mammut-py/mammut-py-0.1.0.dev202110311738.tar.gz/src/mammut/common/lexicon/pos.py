from mammut.common.util import StringEnum
from mammut.common.lexicon.paradigm_producer import ParadigmProducerGroup


class POSType(StringEnum):
    Entity = "entity"
    Event = "event"


class POSdescriptor:
    POS_CLASS_GROUP_COLUMN_NAME = "pos-class-group"
    POS_CLASS_COLUMN_NAME = "pos-class"
    POS_NAME_COLUMN_NAME = "pos-name"
    POS_ID_COLUMN_NAME = "pos-id"
    POS_TYPE_COLUMN_NAME = "pos-type"
    MORPHEME_PARADIGMS_COLUMN_NAME = "morph-paradigms"
    MISSPELLING_PARADIGMS_COLUMN_NAME = "miss-paradigms"
    FEATURES_COLUMN_NAME = "features"
    REGIONAL_SETTINGS_COLUMN_NAME = "regional-settings"
    ARC_COLUMN_NAME = "arc-name"
    POS_ABBREVIATION = "pos-abbreviation"
    POS_SHIFTS = "pos-shifts"

    SHEETS_LOADED = {}

    def __init__(
        self,
        class_group: str,
        pos_class: str,
        name: str,
        id: str,
        pos_type: str,
        morpheme_paradigm_sheet_titles: str,
        misspelling_paradigm_sheet_titles: str,
        feature_paradigm_sheet_titles: str,
        regional_settings: str,
        arc_name: str,
        pos_abbreviation: str,
        pos_shifts: str,
        standard,
    ):
        self.class_group = class_group
        self.pos_class = pos_class
        self.name = name
        self.id = id
        self.pos_type = pos_type
        self.used_regional_settings_list = []
        self.morpheme_paradigms = {}
        self.misspelling_paradigms = {}
        self.feature_paradigms = {}
        self.regional_settings_list = [
            s.strip() for s in regional_settings.split(",") if s.strip()
        ]

        if POSType.contains_value(pos_type):
            self.pos_type = POSType(pos_type)

        self.morpheme_paradigm_sheet_titles_list = [
            s.strip() for s in morpheme_paradigm_sheet_titles.split(",") if s.strip()
        ]
        self.misspelling_paradigm_sheet_titles_list = [
            s.strip() for s in misspelling_paradigm_sheet_titles.split(",") if s.strip()
        ]
        self.feature_paradigm_sheet_titles_list = [
            s.strip() for s in feature_paradigm_sheet_titles.split(",") if s.strip()
        ]
        self.arc_name = arc_name
        self.pos_abbreviation = pos_abbreviation
        self.pos_shifts_ids = [s.strip() for s in pos_shifts.split(",") if s.strip()]
        self.pos_shifts = []
        self.standard = standard
        for (
            morpheme_paradigm_sheet_title_and_rs
        ) in self.morpheme_paradigm_sheet_titles_list:
            if (
                morpheme_paradigm_sheet_title_and_rs != ""
                and ":" in morpheme_paradigm_sheet_title_and_rs
            ):
                regional_setting = morpheme_paradigm_sheet_title_and_rs.split(":")[0]
                morpheme_paradigm_sheet_title = morpheme_paradigm_sheet_title_and_rs.split(
                    ":"
                )[
                    1
                ]
                self.used_regional_settings_list.append(regional_setting)
            elif morpheme_paradigm_sheet_title_and_rs != "":
                if self.regional_settings_list.__len__() == 0:
                    regional_setting = ""
                    morpheme_paradigm_sheet_title = morpheme_paradigm_sheet_title_and_rs
                else:
                    for setting in self.regional_settings_list:
                        if setting in self.used_regional_settings_list:
                            continue
                        if (
                            morpheme_paradigm_sheet_title_and_rs
                            not in POSdescriptor.SHEETS_LOADED
                        ):
                            self.morpheme_paradigms[setting] = ParadigmProducerGroup(
                                morpheme_paradigm_sheet_title_and_rs,
                                self.standard,
                                setting,
                            )
                            POSdescriptor.SHEETS_LOADED[
                                morpheme_paradigm_sheet_title_and_rs
                            ] = self.morpheme_paradigms[setting]
                        else:
                            self.morpheme_paradigms[
                                setting
                            ] = POSdescriptor.SHEETS_LOADED[
                                morpheme_paradigm_sheet_title_and_rs
                            ]
                    continue
            else:
                regional_setting = ""
                morpheme_paradigm_sheet_title = ""
            if morpheme_paradigm_sheet_title not in POSdescriptor.SHEETS_LOADED:
                self.morpheme_paradigms[regional_setting] = ParadigmProducerGroup(
                    morpheme_paradigm_sheet_title, self.standard, regional_setting
                )
                POSdescriptor.SHEETS_LOADED[
                    morpheme_paradigm_sheet_title
                ] = self.morpheme_paradigms[regional_setting]
            else:
                self.morpheme_paradigms[regional_setting] = POSdescriptor.SHEETS_LOADED[
                    morpheme_paradigm_sheet_title
                ]
        self.used_regional_settings_list = []
        for (
            misspelling_paradigm_sheet_title_and_rs
        ) in self.misspelling_paradigm_sheet_titles_list:
            if (
                misspelling_paradigm_sheet_title_and_rs != ""
                and ":" in misspelling_paradigm_sheet_title_and_rs
            ):
                regional_setting = misspelling_paradigm_sheet_title_and_rs.split(":")[0]
                misspelling_paradigm_sheet_title = misspelling_paradigm_sheet_title_and_rs.split(
                    ":"
                )[
                    1
                ]
                self.used_regional_settings_list.append(regional_setting)
            elif misspelling_paradigm_sheet_title_and_rs != "":
                if self.regional_settings_list.__len__() == 0:
                    regional_setting = ""
                    misspelling_paradigm_sheet_title = (
                        misspelling_paradigm_sheet_title_and_rs
                    )
                else:
                    for setting in self.regional_settings_list:
                        if setting in self.used_regional_settings_list:
                            continue
                        if (
                            misspelling_paradigm_sheet_title_and_rs
                            not in POSdescriptor.SHEETS_LOADED
                        ):
                            self.misspelling_paradigms[setting] = ParadigmProducerGroup(
                                misspelling_paradigm_sheet_title_and_rs,
                                self.standard,
                                setting,
                            )
                            POSdescriptor.SHEETS_LOADED[
                                misspelling_paradigm_sheet_title_and_rs
                            ] = self.misspelling_paradigms[setting]
                        else:
                            self.misspelling_paradigms[
                                setting
                            ] = POSdescriptor.SHEETS_LOADED[
                                misspelling_paradigm_sheet_title_and_rs
                            ]
                    continue
            else:
                regional_setting = ""
                misspelling_paradigm_sheet_title = ""
            if misspelling_paradigm_sheet_title not in POSdescriptor.SHEETS_LOADED:
                self.misspelling_paradigms[regional_setting] = ParadigmProducerGroup(
                    misspelling_paradigm_sheet_title, self.standard, regional_setting
                )
                POSdescriptor.SHEETS_LOADED[
                    misspelling_paradigm_sheet_title
                ] = self.misspelling_paradigms[regional_setting]
            else:
                self.misspelling_paradigms[
                    regional_setting
                ] = POSdescriptor.SHEETS_LOADED[misspelling_paradigm_sheet_title]
        self.used_regional_settings_list = []
        for (
            feature_paradigm_sheet_title_and_rs
        ) in self.misspelling_paradigm_sheet_titles_list:
            if (
                feature_paradigm_sheet_title_and_rs != ""
                and ":" in feature_paradigm_sheet_title_and_rs
            ):
                regional_setting = feature_paradigm_sheet_title_and_rs.split(":")[0]
                feature_paradigm_sheet_title = feature_paradigm_sheet_title_and_rs.split(
                    ":"
                )[
                    1
                ]
                self.used_regional_settings_list.append(regional_setting)
            elif feature_paradigm_sheet_title_and_rs != "":
                if self.regional_settings_list.__len__() == 0:
                    regional_setting = ""
                    feature_paradigm_sheet_title = feature_paradigm_sheet_title_and_rs
                else:
                    for setting in self.regional_settings_list:
                        if setting in self.used_regional_settings_list:
                            continue
                        if (
                            feature_paradigm_sheet_title_and_rs
                            not in POSdescriptor.SHEETS_LOADED
                        ):
                            self.feature_paradigms[setting] = ParadigmProducerGroup(
                                feature_paradigm_sheet_title_and_rs,
                                self.standard,
                                setting,
                            )
                            POSdescriptor.SHEETS_LOADED[
                                feature_paradigm_sheet_title_and_rs
                            ] = self.feature_paradigms[setting]
                        else:
                            self.feature_paradigms[
                                setting
                            ] = POSdescriptor.SHEETS_LOADED[
                                feature_paradigm_sheet_title_and_rs
                            ]
                    continue
            else:
                regional_setting = ""
                feature_paradigm_sheet_title = ""
            if feature_paradigm_sheet_title not in POSdescriptor.SHEETS_LOADED:
                self.feature_paradigms[regional_setting] = ParadigmProducerGroup(
                    feature_paradigm_sheet_title, self.standard, regional_setting
                )
                POSdescriptor.SHEETS_LOADED[
                    feature_paradigm_sheet_title
                ] = self.feature_paradigms[regional_setting]
            else:
                self.feature_paradigms[regional_setting] = POSdescriptor.SHEETS_LOADED[
                    feature_paradigm_sheet_title
                ]

    def set_pos_references(self, pos_by_id: dict):
        for pos_id in self.pos_shifts_ids:
            self.pos_shifts.append(pos_by_id[pos_id])

    def __str__(self):
        return f"{self.name}"
