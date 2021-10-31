from collections import UserDict, UserList
from mammut.common.storage.storage_manager import StorageManager
from typing import List, Dict
import pandas as pd


class FunctionalParameterValue:
    def __init__(self, value: str, parameter):
        self.value = value
        self.parameter = parameter


class PrototypicalFunctionalParameterValue(FunctionalParameterValue):
    def __init__(
        self,
        value: str,
        value_type: str,
        show: bool,
        definition: str,
        example: str,
        parameter,
    ):
        FunctionalParameterValue.__init__(self, value, parameter)
        self.value_type = value_type
        self.show = show
        self.definition = definition
        self.example = example


class FunctionalParameterDict(UserDict):
    def __init__(self, standard, spreadsheet_id):
        UserDict.__init__(self)
        self.standard = standard
        self.spreadsheet_id = spreadsheet_id
        self.valid = True
        self.errors = []


class FunctionalParameter:
    def __init__(self, spreadsheet_id: str, standard):
        self.spreadsheet_id = spreadsheet_id
        self.standard = standard
        self.parameter_values = {}


class PrototypicalFunctionalParameter(FunctionalParameter):
    SHEET_NAME = "parameters"
    # PARAMETERS COLUMN NAMES
    CLASS_COLUMN_NAME = "class"
    VALUE_COLUMN_NAME = "value"
    VALUE_TYPE_COLUMN_NAME = "value-type"
    SHOW_COLUMN_NAME = "show"
    DEFINITION_COLUMN_NAME = "definition"
    EXAMPLE_COLUMN_NAME = "example"
    storage_manager = StorageManager()
    DEFAULT_START_CELL = "A1"
    DEFAULT_START_COLUMN = "A"
    DEFAULT_START_ROW = "1"
    DEFAULT_END_CELL = "F503"
    DEFAULT_END_COLUM = "F"

    LOADED_PARAMETERS = {}

    def __init__(self, p_class, group, spreadsheet_id: str, standard):
        FunctionalParameter.__init__(self, spreadsheet_id, standard)
        self.p_class = p_class
        self.group = group
        for ig in self.group.iterrows():
            pv = PrototypicalFunctionalParameterValue(
                ig[1][PrototypicalFunctionalParameter.VALUE_COLUMN_NAME],
                ig[1][PrototypicalFunctionalParameter.VALUE_TYPE_COLUMN_NAME],
                ig[1][PrototypicalFunctionalParameter.SHOW_COLUMN_NAME] != "",
                ig[1][PrototypicalFunctionalParameter.DEFINITION_COLUMN_NAME],
                ig[1][PrototypicalFunctionalParameter.EXAMPLE_COLUMN_NAME],
                self,
            )
            self.parameter_values[pv.value] = pv

    @staticmethod
    def load(spreadsheet_id: str, standard):
        res = None
        if spreadsheet_id in PrototypicalFunctionalParameter.LOADED_PARAMETERS:
            res = PrototypicalFunctionalParameter.LOADED_PARAMETERS[
                spreadsheet_id
            ]
        else:
            res = FunctionalParameterDict(standard, spreadsheet_id)
            res.range_name = (
                PrototypicalFunctionalParameter.SHEET_NAME
                + "!"
                + PrototypicalFunctionalParameter.DEFAULT_START_CELL
            )

            res.data_frame = PrototypicalFunctionalParameter.storage_manager.get_spreadsheet_as_dataframe(
                res.spreadsheet_id,
                PrototypicalFunctionalParameter.SHEET_NAME,
                PrototypicalFunctionalParameter.DEFAULT_START_COLUMN,
                PrototypicalFunctionalParameter.DEFAULT_START_ROW,
                PrototypicalFunctionalParameter.DEFAULT_END_COLUM,
            )

            if res.data_frame is not None:
                res.group_by_object = res.data_frame.groupby(
                    [PrototypicalFunctionalParameter.CLASS_COLUMN_NAME]
                )
                for g in res.group_by_object:
                    prot = PrototypicalFunctionalParameter(
                        g[0], g[1], spreadsheet_id, standard
                    )
                    res[prot.p_class] = prot
            else:
                res.valid = False
                res.errors.append(f"The parameters sheet is not present.")
            PrototypicalFunctionalParameter.LOADED_PARAMETERS[
                spreadsheet_id
            ] = res
        return res


class FunctionalLemmaDefinition:
    def __init__(self, lemma, index):
        self.lemma = lemma
        self.index = index

    def get_description(self):
        raise NotImplementedError()


class PrototypicalFunctionalLemmaDefinition(FunctionalLemmaDefinition):
    # MODEL COLUMN NAMES
    INDEX_COLUMN_NAME = "index"
    HIDE_COLUMN_NAME = "hide"
    PROTOTYPICAL_EXAMPLE_COLUMN_NAME = "prototypical-example"
    COMMENTS_COLUMN_NAME = "comments"
    ETYMOLOGICAL_INDEX_COLUMN_NAME = "etymological-index"
    ETYMOLOGICAL_INFO_COLUMN_NAME = "etymological-info"

    storage_manager = StorageManager()
    DEFAULT_START_CELL = "A1"
    DEFAULT_START_COLUMN = "A"
    DEFAULT_START_ROW = "1"
    DEFAULT_END_CELL = "S503"
    DEFAULT_END_COLUMN = "S"

    LOADED_LEMMAS = {}

    COMMENTS_DEFAULT = "AUN NO ESTA LISTO!!!"
    ETYMOLOGICAL_INDEX_DEFAULT = "-"
    ETYMOLOGICAL_INFO_DEFAULT = "-"

    def __init__(self, lemma, row, spreadsheet_id, parameters, standard):
        FunctionalLemmaDefinition.__init__(
            self,
            lemma,
            row[PrototypicalFunctionalLemmaDefinition.INDEX_COLUMN_NAME],
        )
        self.row = row
        self.prototypical_example = self.row[
            PrototypicalFunctionalLemmaDefinition.PROTOTYPICAL_EXAMPLE_COLUMN_NAME
        ]
        self.comments = PrototypicalFunctionalLemmaDefinition.COMMENTS_DEFAULT
        if (
            PrototypicalFunctionalLemmaDefinition.COMMENTS_COLUMN_NAME
            in self.row
        ):
            self.comments = self.row[
                PrototypicalFunctionalLemmaDefinition.COMMENTS_COLUMN_NAME
            ]
        self.etymological_index = (
            PrototypicalFunctionalLemmaDefinition.ETYMOLOGICAL_INDEX_DEFAULT
        )
        if (
            PrototypicalFunctionalLemmaDefinition.ETYMOLOGICAL_INDEX_COLUMN_NAME
            in self.row
        ):
            self.etymological_index = self.row[
                PrototypicalFunctionalLemmaDefinition.ETYMOLOGICAL_INDEX_COLUMN_NAME
            ]
        self.etymological_info = (
            PrototypicalFunctionalLemmaDefinition.ETYMOLOGICAL_INFO_DEFAULT
        )
        if (
            PrototypicalFunctionalLemmaDefinition.ETYMOLOGICAL_INFO_COLUMN_NAME
            in self.row
        ):
            self.etymological_info = self.row[
                PrototypicalFunctionalLemmaDefinition.ETYMOLOGICAL_INFO_COLUMN_NAME
            ]
        self.spreadsheet_id = spreadsheet_id
        self.parameters = parameters
        self.standard = standard
        self.valid = True
        self.errors = []
        for p in self.parameters:
            paramd = self.parameters[p]
            if p in self.row:
                pv = self.row[p]
                if pv not in paramd.parameter_values:
                    self.valid = False
                    self.errors.append(
                        f"Lemma: {lemma} in spreadsheet: {spreadsheet_id} for index: {self.index} contain a invalid value for parameter: {p}. Value: {pv}"
                    )
                setattr(self, p, pv)
            else:
                self.valid = False
                self.errors.append(
                    f"Lemma: {lemma} in spreadsheet: {spreadsheet_id} for index: {self.index} does not contain parameter: {p}"
                )

    def get_description(self):
        res = f"Ejemplo prototipico: {self.prototypical_example}\nComentarios: {self.comments}"
        for p in self.parameters:
            pv = getattr(self, p)
            paramd = self.parameters[p]
            descriptor = paramd.parameter_values[pv]
            if descriptor.show:
                res += f"\n{descriptor.value_type}: {pv}"
        return res

    @staticmethod
    def get_definitions(
        lemma,
        model_parameters_spreadsheet_id: str,
        model_spreadsheet_id: str,
        standard,
    ):
        parameters = PrototypicalFunctionalParameter.load(
            model_parameters_spreadsheet_id, standard
        )
        res = None
        loading_id = f"{model_spreadsheet_id}---{lemma}"
        if loading_id in PrototypicalFunctionalLemmaDefinition.LOADED_LEMMAS:
            res = PrototypicalFunctionalLemmaDefinition.LOADED_LEMMAS[
                loading_id
            ]
        else:
            res = FunctionalLemmaDefinitionList(standard, model_spreadsheet_id)
            if not parameters.valid:
                res.valid = False
                res.errors = res.errors + parameters.errors
            res.range_name = (
                lemma
                + "!"
                + PrototypicalFunctionalLemmaDefinition.DEFAULT_START_CELL
            )

            res.data_frame = PrototypicalFunctionalLemmaDefinition.storage_manager.get_spreadsheet_as_dataframe(
                res.spreadsheet_id,
                lemma,
                PrototypicalFunctionalLemmaDefinition.DEFAULT_START_COLUMN,
                PrototypicalFunctionalLemmaDefinition.DEFAULT_START_ROW,
                PrototypicalFunctionalLemmaDefinition.DEFAULT_END_COLUMN,
            )

            if (
                PrototypicalFunctionalLemmaDefinition.HIDE_COLUMN_NAME
                in res.data_frame
            ):
                res.data_frame = res.data_frame[
                    res.data_frame[
                        PrototypicalFunctionalLemmaDefinition.HIDE_COLUMN_NAME
                    ]
                    == ""
                ]
            if res.data_frame is not None:
                for r in res.data_frame.iterrows():
                    defi = PrototypicalFunctionalLemmaDefinition(
                        lemma, r[1], model_spreadsheet_id, parameters, standard
                    )
                    res.append(defi)
                    if not defi.valid:
                        res.valid = False
                        res.errors = res.errors + defi.errors

            else:
                res.valid = False
                res.errors.append(
                    f"The protypical definitions sheet is not present."
                )
            PrototypicalFunctionalLemmaDefinition.LOADED_LEMMAS[
                loading_id
            ] = res
        return res


class FunctionalLemmaDescriptor:
    LEMMA_COLUMN_NAME = "lemma"
    HIDE_COLUMN_NAME = "hide"
    WORD_TYPE_COLUMN_NAME = "word-type"
    REGIONAL_SETTINGS_LEMMA_COLUMN_NAME = "regional-settings-lemma"
    POS_PARADIGM_COLUMN_NAME = "pos-paradigm"
    MODEL_TYPE_COLUMN_NAME = "model-type"
    MODEL_PARAMETERS_SPREADSHEET_ID_COLUMN_NAME = (
        "model-parameters-spreadsheet-id"
    )
    MODEL_SPREADSHEET_ID_COLUMN_NAME = "model-spreadsheet-id"
    MORPH_PARADIGM_COLUMN_NAME = "morph-paradigm"
    BOUND_MORPH_COLUMN_NAME = "bound-morph"
    MISS_PARADIGM_COLUMN_NAME = "miss-paradigm"
    FET_PARADIGM_COLUMN_NAME = "fet-paradigm"
    FEATURE_CLASS_COLUMN_NAME = "feature-class"
    FEATURE_ID_COLUMN_NAME = "feature-id"
    FEATURE_POS_COLUMN_NAME = "feature-pos-tag"
    DEFAULT_START_CELL = "A1"
    DEFAULT_START_COLUMN = "A"
    DEFAULT_START_ROW = "1"
    DEFAULT_END_CELL = "O"

    def __init__(self, dataframe_row, standard):
        self.lemma = (
            dataframe_row[FunctionalLemmaDescriptor.LEMMA_COLUMN_NAME]
            .lower()
            .strip()
        )
        self.word_type = dataframe_row[
            FunctionalLemmaDescriptor.WORD_TYPE_COLUMN_NAME
        ]
        self.regional_settings_lemma = dataframe_row[
            FunctionalLemmaDescriptor.REGIONAL_SETTINGS_LEMMA_COLUMN_NAME
        ]
        self.pos_paradigm = dataframe_row[
            FunctionalLemmaDescriptor.POS_PARADIGM_COLUMN_NAME
        ]
        self.model_type = dataframe_row[
            FunctionalLemmaDescriptor.MODEL_TYPE_COLUMN_NAME
        ]
        self.model_parameters_spreadsheet_id = dataframe_row[
            FunctionalLemmaDescriptor.MODEL_PARAMETERS_SPREADSHEET_ID_COLUMN_NAME
        ]
        self.model_spreadsheet_id = dataframe_row[
            FunctionalLemmaDescriptor.MODEL_SPREADSHEET_ID_COLUMN_NAME
        ]
        self.morph_paradigm = dataframe_row[
            FunctionalLemmaDescriptor.MORPH_PARADIGM_COLUMN_NAME
        ]
        self.is_bound = bool(
            dataframe_row[FunctionalLemmaDescriptor.BOUND_MORPH_COLUMN_NAME]
        )
        self.miss_paradigm = dataframe_row[
            FunctionalLemmaDescriptor.MISS_PARADIGM_COLUMN_NAME
        ]
        self.fet_paradigm = dataframe_row[
            FunctionalLemmaDescriptor.FET_PARADIGM_COLUMN_NAME
        ]
        self.feature_class = dataframe_row[
            FunctionalLemmaDescriptor.FEATURE_CLASS_COLUMN_NAME
        ]
        self.feature_id = dataframe_row[
            FunctionalLemmaDescriptor.FEATURE_ID_COLUMN_NAME
        ]
        self.feature_pos = dataframe_row[
            FunctionalLemmaDescriptor.FEATURE_POS_COLUMN_NAME
        ]
        self.standard = standard
        self.id = self.build_id(
            self.lemma, self.regional_settings_lemma, self.pos_paradigm
        )
        self.implicit_condition_id = None
        if not self.is_explicit():
            self.implicit_condition_id = self.build_implicit_condition_id(
                self.feature_class,
                self.feature_id,
                self.feature_pos,
                self.regional_settings_lemma,
            )
        self.definitions = []
        self.undefined = False
        self.valid = True
        self.errors = []
        if self.model_type == "prototypical":
            self.definitions = PrototypicalFunctionalLemmaDefinition.get_definitions(
                self.lemma,
                self.model_parameters_spreadsheet_id,
                self.model_spreadsheet_id,
                self.standard,
            )
            if not self.definitions.valid:
                self.valid = False
                self.errors = self.errors + self.definitions.errors
        elif (
            self.model_type == ""
            and self.model_parameters_spreadsheet_id == ""
            and self.model_spreadsheet_id == ""
        ):
            self.undefined = True
        else:
            self.valid = False
            self.errors.append(f"The model type is invalid.")

    def is_explicit(self):
        return not self.feature_class

    @staticmethod
    def build_implicit_condition_id(
        feature_class: str,
        feature_id: str,
        feature_pos: str,
        regional_settings_lemma: str,
    ):
        return f"{feature_class}-{feature_id}-{feature_pos}-{regional_settings_lemma}"

    @staticmethod
    def build_id(lemma: str, regional_settings_lemma: str, pos_paradigm: str):
        return f"{lemma}-{regional_settings_lemma}-{pos_paradigm}"


class FunctionalLemmaDefinitionList(UserList):
    def __init__(self, standard, spreadsheet_id, initlist=None):
        UserList.__init__(self, initlist)
        self.standard = standard
        self.spreadsheet_id = spreadsheet_id
        self.valid = True
        self.errors = []


class FunctionalModelComparison:
    """Compare a prototypical modeling with another modeling of the same type."""

    storage_manager = StorageManager()

    def __init__(self, item_name: str, sheet_id: str):
        self.item_name = item_name
        self.sheet_id = sheet_id
        self.start_position = ("A", "1")
        self.end_position = "I"
        self.pivot = False
        self.model = self._get_model_from_sheets(self.sheet_id, self.item_name)

    def _get_model_from_sheets(
        self, sheet_id: str, item_name: str
    ) -> pd.DataFrame:
        """Get model from sheet_ID."""
        return FunctionalModelComparison.storage_manager.get_spreadsheet_as_dataframe(
            sheet_id,
            item_name,
            self.start_position[0],
            self.start_position[1],
            self.end_position,
            self.pivot,
        )

    def _merge_df(
        self, model1: pd.DataFrame, model2: pd.DataFrame, features: List
    ) -> pd.DataFrame:
        """Merge two dataframes from a join operation based on the features parameter."""
        return model1.merge(
            model2,
            how="inner",
            indicator=True,
            on=features,
            suffixes=["_model", "_alt"],
        )

    def duplicates_in_model(self, features: List) -> pd.DataFrame:
        """Find repeated modeling in the prototypical model."""
        try:
            return self.model[self.model.loc[:, features].duplicated(keep=False)]
        except KeyError as e:
            return f"Error. Column not found. See {str(e)}"

    def non_duplicates_in_model(self, features: List) -> pd.DataFrame:
        """Find an example of each non-duplicate modeling in the model."""
        try:
            return self.model[~self.model.loc[:, features].duplicated()]
        except KeyError as e:
            return f"Error. Column not found. See {str(e)}"

    def compare_to(self, item_name: str, features: List) -> pd.DataFrame:
        """It compares the current model with another model and returns the modelings in common."""
        self.alternative_model = self._get_model_from_sheets(
            self.sheet_id, item_name
        )
        model1 = self.model[~self.model.loc[:, features].duplicated()]
        model2 = self.alternative_model[
            ~self.alternative_model.loc[:, features].duplicated()
        ]
        return self._merge_df(model1, model2, features)

    def compare_to_list(
        self, models: List, features: List, join: bool = False
    ) -> Dict[str, pd.DataFrame]:
        """It compares the current model with another models (from a list) and returns the modelings in common."""
        model_dfs = {}
        original_dfs = []
        for item_name in models:
            alt_model = self._get_model_from_sheets(self.sheet_id, item_name)
            model1 = self.model[
                ~self.model.loc[:, features].duplicated()
            ].copy()
            model1["item_name"] = self.item_name
            model2 = alt_model[~alt_model.loc[:, features].duplicated()].copy()
            model2["item_name"] = item_name
            merged_model = self._merge_df(model1, model2, features)
            model_dfs[item_name] = merged_model
            original_dfs.append(model2)

        if join:
            joined_dfs = pd.concat(original_dfs)
            joined = joined_dfs[
                ~joined_dfs.loc[:, features].duplicated().copy()
            ]
            merged_joined = self._merge_df(self.model, joined, features)
            model_dfs["__all__"] = merged_joined
        return model_dfs
