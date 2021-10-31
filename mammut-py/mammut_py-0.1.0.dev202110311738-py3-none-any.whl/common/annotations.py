# coding=utf-8
from brat_widget.widget import Visualizer, Annotator
from brat_widget.document import *
from brat_widget.configuration import *
import pandas as pd
from mammut.common.storage.storage_manager import StorageManager


class Restitution:
    SHEET_TITTLE = "restitutions"

    def __init__(self, package, spreadsheet_id):
        self.package = package
        self.spreadsheet_id = spreadsheet_id
        self.storage_manager = StorageManager()

    def add_restitution(
        self, corpus_name, scenario_id, event_id, extension_id, restitution
    ):  # definir tipos, corpusEvent y str
        restitution_id = (
            corpus_name
            + "-"
            + str(scenario_id)
            + "-"
            + str(event_id)
            + "-"
            + str(extension_id)
        )
        row = [restitution_id, restitution]
        current_id = self.storage_manager.append_row_to_sheet(
            self.spreadsheet_id, Restitution.SHEET_TITTLE, row
        )
        # de aqui saco el id y se le agrega para saber cual es la restitucion del evento
        df = self.package.annotations.restitution_data_frame
        self.package.annotations.restitution_data_frame = df.append(
            pd.Series(row, list(df.columns)), ignore_index=True
        )
        return current_id

    def delete_restitutions(self, event_annotation):
        df = self.package.annotations.restitution_data_frame
        rows_indices = df[df["id"] == event_annotation.get_id()].index.tolist()
        rows_to_delete = len(rows_indices)
        self.package.annotations.restitution_data_frame = self.package.annotations.restitution_data_frame.drop(
            rows_indices
        )
        self.package.annotations.restitution_data_frame = self.package.annotations.restitution_data_frame.reset_index(
            drop=True
        )
        while rows_to_delete > 0:
            self.delete_restitution_from_sheet(rows_indices[0])
            rows_to_delete = rows_to_delete - 1
        deleted_restitutions = len(rows_indices)
        return deleted_restitutions

    def delete_restitution_from_sheet(self, row):
        response = self.storage_manager.delete_rows_from_spreadsheet(
            self.spreadsheet_id, "restitutions", str(row + 1), str(row + 2)
        )
        # TODO poner dos com constante es por el rowque ocupan los titulos y la cuenta del sheet empieza en 1
        return response


class MammutEventAnnotation:

    SCENARIO_INDEX_ID = "scenery"
    EVENT_ENTRY_INDEX_ID = "event_entry"

    def __init__(self, package, event_info):
        self.package = package
        self.standard = package.standard
        self.spreadsheet_id = package.spreadsheet_id
        self.dimensions = package.standard.dimensiones_descriptor_list
        self.dimensions_index = {k: i for i, k in enumerate(self.dimensions.keys())}
        self.event = event_info
        self.is_annotated_dimention = {}
        self.storage_manager = StorageManager()
        for i in self.dimensions:
            self.is_annotated_dimention[i] = False

        self.documents_by_dimension = {}
        self.configurations_by_dimension = {}
        self.range_dimension = {}

    def load_range(self, data_frame, dimension, annotations):
        matching_ids = data_frame[data_frame["id"] == self.get_id()].index.tolist()
        if len(matching_ids) > 0:

            if dimension not in annotations.sorted_ranges_by_dimension:
                annotations.sorted_ranges_by_dimension[dimension] = []
            range_order_object = {
                dimension: {
                    self.get_id(): {
                        "range": (matching_ids[0], matching_ids[-1]),
                        "order_index": len(
                            annotations.sorted_ranges_by_dimension[dimension]
                        ),
                    }
                }
            }
            if (
                range_order_object
                not in annotations.sorted_ranges_by_dimension[dimension]
            ):
                annotations.sorted_ranges_by_dimension[dimension].append(
                    range_order_object
                )
            if dimension not in annotations.ranges_by_dimension:
                annotations.ranges_by_dimension[dimension] = {}
            if self.get_id() not in annotations.ranges_by_dimension[dimension]:
                annotations.ranges_by_dimension[dimension][self.get_id()] = {
                    "range": (matching_ids[0], matching_ids[-1]),
                    "order_index": annotations.sorted_ranges_by_dimension[
                        dimension
                    ].index(range_order_object),
                }
            return

        if (
            dimension not in annotations.ranges_by_dimension
        ):  # TODO esto es necesario??? en la linea enterior habia un print(get_id()) revisar
            annotations.ranges_by_dimension[dimension] = {}
        annotations.ranges_by_dimension[dimension][self.get_id()] = {
            "range": None,
            "order_index": None,
        }

    def load_configurations_and_documents(self, dimensions):
        for i in dimensions:
            self.initialize_configuration(i)
            self.initialize_document(i, self.event)

    def update_documents_after_restitution(self, restitution):
        self.event["original_text"] = restitution + " " + self.event["original_text"]
        self.load_configurations_and_documents(self.dimensions)
        for i in self.dimensions:
            self.is_annotated_dimention[i] = False

    def update_documents_after_delete_restitution(self, deleted_restitutions: int):
        restitutions = self.event["original_text"].split(" ")[:deleted_restitutions]
        self.event["original_text"] = " ".join(
            self.event["original_text"].split(" ")[deleted_restitutions:]
        )
        self.load_configurations_and_documents(self.dimensions)
        for i in self.dimensions:
            self.is_annotated_dimention[i] = False
        return restitutions

    def initialize_configuration(self, dimension):
        self.configurations_by_dimension[
            dimension
        ] = self.standard.get_annotation_dimension_class(dimension)
        self.configurations_by_dimension[dimension].initialize()

    def initialize_document(self, dimension, event):
        corpus = self.package.corpus_map.get_corpus_by_type(
            event["corpus"]["type"], event["corpus"]["name"]
        )
        # TODO: this update the original_text from tokenized_mesage so is painted in the anotator/ same for visualizer
        corpus.sceneries[event[MammutEventAnnotation.SCENARIO_INDEX_ID]].events[
            event[MammutEventAnnotation.EVENT_ENTRY_INDEX_ID]
        ].tokenized_messages[event["tokenized_message_index"]].original_text = event[
            "original_text"
        ]
        # TODO: se deben devol;ver los diferentses mesaeges cuando los hay
        self.documents_by_dimension[dimension] = (
            corpus.sceneries[event[MammutEventAnnotation.SCENARIO_INDEX_ID]]
            .events[event[MammutEventAnnotation.EVENT_ENTRY_INDEX_ID]]
            .get_annotation_documents(self.configurations_by_dimension[dimension])[0]
        )
        self.documents_by_dimension[dimension].initialize()

    def get_annotator(self, dimension, event):
        annotator = Annotator(
            value=self.documents_by_dimension[dimension],
            collection_configuration=self.configurations_by_dimension[dimension],
            general_configuration=GeneralConfiguration(),
        )
        return annotator

    def get_visualizer(self, dimension, event):
        visualizer = Visualizer(
            value=self.documents_by_dimension[dimension],
            collection_configuration=self.configurations_by_dimension[dimension],
        )
        return visualizer

    def get_annotations_elements(self, dimension):
        dimension_index = list(self.dimensions).index(dimension)
        if dimension_index != 0:
            required_dimension_annotation = list(self.dimensions)[:dimension_index][-1]
        else:
            required_dimension_annotation = None
        annotation_elements = []
        if required_dimension_annotation is None:
            annotation_elements.append(self.get_annotator(dimension, self.event))
        elif self.is_annotated_dimention[
            required_dimension_annotation
        ]:  # itera hasta la dimension que se indique
            for index, i in enumerate(self.dimensions):
                if self.is_annotated_dimention[i] and i != dimension:
                    annotation_elements.append(self.get_visualizer(i, self.event))
                else:
                    annotation_elements.append(self.get_annotator(i, self.event))
                    break
        else:  # itera hasta la ultima dimension valida
            for index, i in enumerate(self.dimensions):
                if self.is_annotated_dimention[i] and index != len(self.dimensions) - 1:
                    annotation_elements.append(self.get_visualizer(i, self.event))
                else:
                    annotation_elements.append(self.get_annotator(i, self.event))
                    break
        return annotation_elements

    def current_dimension(self, dimension):
        dimension_index = list(self.dimensions).index(dimension)
        if dimension_index != 0:
            required_dimension_annotation = list(self.dimensions)[:dimension_index][-1]
        else:
            required_dimension_annotation = None
        if required_dimension_annotation is None:
            return dimension
        elif self.is_annotated_dimention[required_dimension_annotation]:
            return dimension

        for i in self.is_annotated_dimention:
            if not self.is_annotated_dimention[i]:
                return i
        return None

    def set_rows_for_persist(self, ann_obj):
        annotation_rows = []
        for index, i in enumerate(ann_obj.get_textbounds()):
            annotation_row = self.get_row_from_text_bound_annotation(i)
            annotation_rows.append(annotation_row)
        sorted_events = self.get_dependent_sorted_events(ann_obj)
        for i in sorted_events:
            annotation_rows = annotation_rows + self.get_rows_from_event_annotation(
                i, ann_obj
            )
        for i in ann_obj.get_attributes():
            annotation_rows.append(self.get_row_from_attribute_annotation(i, ann_obj))
        return annotation_rows

    def get_row_from_text_bound_annotation(self, entity):
        annotation_row = list()
        annotation_row.append(self.get_id())
        annotation_row.append(entity.text)
        annotation_row.append(
            str(entity.spans[0][0]) + "," + str(entity.spans[0][1])
        )  # TODO:siempre es uno??
        self.package.annotations.mammut_id_brat_id_dict[
            self.get_id_from_brat_entity(
                (entity.spans[0][0], entity.spans[0][1]), entity.type
            )
        ] = entity.id
        annotation_row.append(entity.type)
        annotation_row.append("")
        annotation_row.append("")
        annotation_row.append("")
        annotation_row.append("")
        annotation_row.append("")
        annotation_row.append(MammutAnnotations.ANNOTATION_ENTITY_TYPE)
        return annotation_row

    def get_rows_from_event_annotation(self, event, ann_obj):
        event_rows = []
        annotation_row = [self.get_id(), "", "", ""]
        for arg in event.args:
            annotation_row.append(
                self.get_id_from_brat_entity(
                    ann_obj.get_ann_by_id(event.trigger).spans[0],
                    ann_obj.get_ann_by_id(event.trigger).type,
                )
            )
            if arg[1].startswith(
                "E"
            ):  # TODO:como se que es un evento??validar si el objeto tiene algo para validar?
                entity = ann_obj.get_ann_by_id(ann_obj.get_ann_by_id(arg[1]).trigger)
                annotation_row.append(
                    self.get_id_from_brat_entity(entity.spans[0], entity.type)
                )
            else:
                annotation_row.append(
                    self.get_id_from_brat_entity(
                        ann_obj.get_ann_by_id(arg[1]).spans[0],
                        ann_obj.get_ann_by_id(arg[1]).type,
                    )
                )
            annotation_row.append("")
            annotation_row.append("")
            annotation_row.append("")
            annotation_row.append(MammutAnnotations.ANNOTATION_EVENT_TYPE)
            event_rows.append(annotation_row)
            annotation_row = [self.get_id(), "", "", ""]
        return event_rows

    def get_row_from_attribute_annotation(self, attribute, ann_obj):
        annotation_row = [self.get_id(), "", "", "", "", ""]
        annotation_row.append(attribute.type)
        if isinstance(ann_obj.get_ann_by_id(attribute.target), EventAnnotation):
            target_id = ann_obj.get_ann_by_id(attribute.target).trigger
        else:
            target_id = attribute.target
        annotation_row.append(
            self.get_id_from_brat_entity(
                ann_obj.get_ann_by_id(target_id).spans[0],
                ann_obj.get_ann_by_id(target_id).type,
            )
        )
        annotation_row.append(attribute.value)
        annotation_row.append(MammutAnnotations.ANNOTATION_FEATURE_TYPE)
        return annotation_row

    def get_dependent_sorted_events(self, ann_obj):
        nested_events = list()
        simple_events = list()
        for event in ann_obj.get_events():
            is_nested = False
            for arg in event.args:
                if arg[1].startswith("E"):  # TODO:si es un evento
                    is_nested = True
                    break
            if is_nested:
                nested_events.append(event)
            else:
                simple_events.append(event)
        # TODO:puedo meter esto en el segundo for en lugar de volver a iterar sobre los nestedevents
        event_ids = [
            event.id for event in nested_events
        ]  # TODO:podria ser un diccionario?
        event_ids_dict = {event.id: event for event in nested_events}
        for event in nested_events:
            for arg in event.args:
                if arg[1] in event_ids:  # si el argumento es parte de los nested events
                    arg_index = event_ids.index(arg[1])
                    current_event_index = event_ids.index(event.id)
                    if (
                        arg_index > current_event_index
                    ):  # si el indice/posicoin del argumento es mayor que la del evento actual cambiamos la posicion
                        event_ids[arg_index], event_ids[current_event_index] = (
                            event_ids[current_event_index],
                            event_ids[arg_index],
                        )
        sorted_nested_events = [
            event_ids_dict[id_index] for id_index in event_ids
        ]  # event_ids en este punto esta ordenado
        return simple_events + sorted_nested_events

    def get_id(self):
        annotation_id = (
            self.event["corpus"]["name"]
            + "-"
            + str(self.event[MammutEventAnnotation.SCENARIO_INDEX_ID])
            + "-"
            + str(self.event[MammutEventAnnotation.EVENT_ENTRY_INDEX_ID])
            + "-"
            + str(self.event["tokenized_message_index"])
        )
        return annotation_id

    def get_id_from_brat_entity(self, span: tuple, pos: str):
        return self.get_id() + "-" + str(span[0]) + "-" + str(span[1]) + "-" + pos

    def add_annotation_to_sheet(self, dimension):
        delete_result, num_of_deleted_cells = self.delete_annotation_from_sheet(
            dimension
        )
        rows = self.set_rows_for_persist(self.documents_by_dimension[dimension].ann_obj)
        new_range = []
        for index, row in enumerate(rows):
            result = self.storage_manager.append_row_to_sheet(
                self.spreadsheet_id,
                self.package.annotations.default_annotation_dimensions[dimension],
                row,
            )
            if len(rows) == 1:
                new_range.append(
                    int(
                        result["updates"]["updatedRange"].split(
                            MammutAnnotations.DEFAULT_ANNOTATIONS_END_CELL
                        )[1]
                    )
                    - 2
                )
                new_range.append(
                    int(
                        result["updates"]["updatedRange"].split(
                            MammutAnnotations.DEFAULT_ANNOTATIONS_END_CELL
                        )[1]
                    )
                    - 2
                )
            elif index == 0:
                new_range.append(
                    int(
                        result["updates"]["updatedRange"].split(
                            MammutAnnotations.DEFAULT_ANNOTATIONS_END_CELL
                        )[1]
                    )
                    - 2
                )
            elif index == len(rows) - 1:
                new_range.append(
                    int(
                        result["updates"]["updatedRange"].split(
                            MammutAnnotations.DEFAULT_ANNOTATIONS_END_CELL
                        )[1]
                    )
                    - 2
                )
        self.package.annotations.update_ranges(
            (new_range[0], new_range[1]),
            dimension,
            self.get_id(),
            jump=num_of_deleted_cells,
        )
        self.is_annotated_dimention[dimension] = True

    def delete_annotation_from_sheet(self, dimension):
        num_of_deleted_cells = 0
        if (
            self.package.annotations.ranges_by_dimension[dimension][self.get_id()][
                "range"
            ]
            is not None
        ):
            num_of_deleted_cells = (
                self.package.annotations.ranges_by_dimension[dimension][self.get_id()][
                    "range"
                ][-1]
                - self.package.annotations.ranges_by_dimension[dimension][
                    self.get_id()
                ]["range"][0]
            )
            delete_response = self.storage_manager.delete_rows_from_spreadsheet(
                self.spreadsheet_id,
                self.package.annotations.default_annotation_dimensions[dimension],
                str(
                    self.package.annotations.ranges_by_dimension[dimension][
                        self.get_id()
                    ]["range"][0]
                    + 1
                ),
                str(
                    self.package.annotations.ranges_by_dimension[dimension][
                        self.get_id()
                    ]["range"][-1]
                    + 2
                ),
            )  # TODO poner dos com constante es por el rowque ocupan los titulos y la cuenta del sheet empieza en 1
        else:
            delete_response = None
        return delete_response, num_of_deleted_cells


class MammutAnnotations:
    DEFAULT_RESTITUTIONS_START_COLUMN = "A"
    DEFAULT_RESTITUTIONS_START_ROW = "1"
    DEFAULT_RESTITUTIONS_END_CELL = "B"
    DEFAULT_ANNOTATIONS_START_COLUMN = "A"
    DEFAULT_ANNOTATIONS_START_ROW = "1"
    DEFAULT_ANNOTATIONS_END_CELL = "J"
    DEFAULT_RESTITUTIONS_SHEET_NAME = "restitutions"
    ANNOTATION_ENTITY_TYPE = "entity"
    ANNOTATION_EVENT_TYPE = "event"
    ANNOTATION_FEATURE_TYPE = "feature"
    NO_VARIABLE_ID_PARAMS = 3
    storage_manager = StorageManager()

    def __init__(self, package):
        self.package = package
        self.spreadsheet_id = package.spreadsheet_id
        self.event_annotations = []
        self.events_by_corpus = {}
        self.annotation_event_by_corpus = {}
        # TODO: poner restitutions strin en constante
        self.restitution_data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
            self.spreadsheet_id,
            self.DEFAULT_RESTITUTIONS_SHEET_NAME,
            self.DEFAULT_RESTITUTIONS_START_COLUMN,
            self.DEFAULT_RESTITUTIONS_START_ROW,
            self.DEFAULT_RESTITUTIONS_END_CELL,
        )
        self.ranges_by_dimension = {}
        self.sorted_ranges_by_dimension = {}
        self.annotation_data_frames = {}
        self.mammut_id_brat_id_dict = {}
        self.mammut_id_event_brat_id_dict = {}
        self.default_annotation_dimensions = {}
        for dimension in package.standard.dimensiones_descriptor_list:
            self.default_annotation_dimensions[dimension] = "a-" + dimension
            self.sorted_ranges_by_dimension[dimension] = []
        self.load_annotations_data_frames()
        self.load_events()
        self.load_annotation_events()
        self.load_restitutions()
        self.load_events_configurations()
        self.load_saved_annotations()
        self.sort_ranges_list()

    def update_ranges(self, new_range, dimension, id, jump=None, only_delete=False):
        add_new_range_object = False

        if jump is None:
            jump = new_range[1] - new_range[0] + 1
        else:
            jump = jump + 1

        changed_index = self.ranges_by_dimension[dimension][id]["order_index"]
        if changed_index is None:
            changed_index = len(self.sorted_ranges_by_dimension[dimension]) - 1
            add_new_range_object = True
        for i in self.sorted_ranges_by_dimension[dimension][changed_index + 1 :]:
            # TODO las dos lineas que vienen modifican dos cosas diferentess????
            self.ranges_by_dimension[dimension][list(i[dimension].keys())[0]][
                "order_index"
            ] = (
                self.ranges_by_dimension[dimension][list(i[dimension].keys())[0]][
                    "order_index"
                ]
                - 1
            )
            i[dimension][list(i[dimension].keys())[0]]["order_index"] = (
                i[dimension][list(i[dimension].keys())[0]]["order_index"] - 1
            )
            update_range = []
            if (
                self.ranges_by_dimension[dimension][list(i[dimension].keys())[0]][
                    "range"
                ][0]
                - jump
                <= 0
            ):
                jump = self.ranges_by_dimension[dimension][
                    list(i[dimension].keys())[0]
                ]["range"][0]
            update_range.append(
                self.ranges_by_dimension[dimension][list(i[dimension].keys())[0]][
                    "range"
                ][0]
                - jump
            )
            update_range.append(
                self.ranges_by_dimension[dimension][list(i[dimension].keys())[0]][
                    "range"
                ][1]
                - jump
            )
            self.ranges_by_dimension[dimension][list(i[dimension].keys())[0]][
                "range"
            ] = tuple(update_range)
            i[dimension][list(i[dimension].keys())[0]]["range"] = tuple(update_range)
        if not add_new_range_object:
            range_object = self.sorted_ranges_by_dimension[dimension].pop(changed_index)
            range_object[dimension][id]["order_index"] = len(
                self.sorted_ranges_by_dimension[dimension]
            )
            range_object[dimension][id]["range"] = new_range
        else:
            range_object = {
                dimension: {
                    id: {
                        "range": new_range,
                        "order_index": len(self.sorted_ranges_by_dimension[dimension]),
                    }
                }
            }
        if only_delete:
            self.ranges_by_dimension[dimension][id]["range"] = None
            self.ranges_by_dimension[dimension][id]["order_index"] = None
        else:
            self.sorted_ranges_by_dimension[dimension].append(range_object)
            self.ranges_by_dimension[dimension][id]["range"] = new_range
            self.ranges_by_dimension[dimension][id]["order_index"] = (
                len(self.sorted_ranges_by_dimension[dimension]) - 1
            )

    # TODO: revisar si es necesario el arreglo sorted_blah_vlah, no se podra ordenar de manera mas sencilla el diccionario????
    def sort_ranges_list(self):  # TODO: mejorar el tiempo de ejecucion de este metodo
        bigest_index = 0
        aux_range = (0, 0)
        aux_list = []
        for dimension in self.default_annotation_dimensions:
            while len(self.sorted_ranges_by_dimension[dimension]) > 0:

                for index, j in enumerate(self.sorted_ranges_by_dimension[dimension]):
                    if (
                        j[dimension][list(j[dimension].keys())[0]]["range"][0]
                        >= aux_range[1]
                    ):
                        aux_range = j[dimension][list(j[dimension].keys())[0]]["range"]
                        bigest_index = index
                aux_list.append(
                    self.sorted_ranges_by_dimension[dimension].pop(bigest_index)
                )
                bigest_index = 0
                aux_range = (0, 0)

                # TODO:en la linea superior, se reduce el size del array y se guarda el valor de indice del mayor, y cuando termina busca un indice que ya no existe
            self.sorted_ranges_by_dimension[dimension] = aux_list[
                ::-1
            ]  # reversed aux list
            for order_index, elem in enumerate(
                self.sorted_ranges_by_dimension[dimension]
            ):
                for id in elem[dimension]:
                    elem[dimension][id]["order_index"] = order_index
                    self.ranges_by_dimension[dimension][id]["order_index"] = order_index
            aux_list = []

    def load_annotations_data_frames(self):
        for i in self.default_annotation_dimensions:
            self.annotation_data_frames[
                i
            ] = self.storage_manager.get_spreadsheet_as_dataframe(
                self.spreadsheet_id,
                self.default_annotation_dimensions[i],
                self.DEFAULT_ANNOTATIONS_START_COLUMN,
                self.DEFAULT_ANNOTATIONS_START_ROW,
                self.DEFAULT_ANNOTATIONS_END_CELL,
            )

    def load_events(self):
        for corpus in self.package.corpus_map.get_all_corpus():
            if corpus.annotable:
                self.events_by_corpus[corpus.sheet_title] = []
                event_message_info = {}
                for scenario in corpus.sceneries:
                    for event_entry_index, event_entry in enumerate(
                        corpus.sceneries[scenario].events
                    ):
                        for tokenized_message_index, tokenized_message in enumerate(
                            event_entry.tokenized_messages
                        ):
                            event_message_info["corpus"] = {
                                "type": type(corpus),
                                "name": corpus.sheet_title,
                            }  # TODO mejorar estructura de este "event", deberia definirse asi y aqui?
                            event_message_info[
                                MammutEventAnnotation.SCENARIO_INDEX_ID
                            ] = scenario
                            event_message_info[
                                MammutEventAnnotation.EVENT_ENTRY_INDEX_ID
                            ] = event_entry_index
                            event_message_info[
                                "tokenized_message_index"
                            ] = tokenized_message_index
                            event_message_info[
                                "original_text"
                            ] = tokenized_message.original_text
                            event_message_info[
                                "regnional_settings"
                            ] = event_entry.str_regional_settings
                            self.events_by_corpus[corpus.sheet_title].append(
                                event_message_info
                            )
                            event_message_info = {}

    def load_annotation_events(
        self,
    ):  # TODO: esto podria hacerse de una sola vez en metodo load_events
        for corpus_name in self.events_by_corpus:
            self.annotation_event_by_corpus[corpus_name] = []
            for event in self.events_by_corpus[corpus_name]:
                event_annotation = MammutEventAnnotation(self.package, event)
                for dimension in self.default_annotation_dimensions:
                    event_annotation.load_range(
                        self.annotation_data_frames[dimension], dimension, self
                    )
                self.annotation_event_by_corpus[corpus_name].append(event_annotation)

    def load_restitutions(self):
        for i in self.restitution_data_frame.iterrows():
            restitution_id = i[1][0]
            restitution = i[1][1]
            (
                corpus,
                scenario,
                event_entry,
                tokenized_message_index,
            ) = self.parse_restitution_id(restitution_id)
            annotation_event = self.get_event_by_parsed_id(
                corpus, scenario, event_entry, tokenized_message_index
            )
            self.add_restitution_to_anotation_event(restitution, annotation_event)

    def load_events_configurations(self):
        for i in self.annotation_event_by_corpus:
            for j in self.annotation_event_by_corpus[i]:
                j.load_configurations_and_documents(self.default_annotation_dimensions)

    def load_saved_annotations(self):
        for dimension in self.annotation_data_frames:
            if (
                dimension in self.annotation_data_frames
                and self.annotation_data_frames[dimension] is not None
            ):
                for j in self.annotation_data_frames[dimension].iterrows():
                    annotation_id = j[1][0]
                    text = j[1][1]
                    span = j[1][2]
                    pos = j[1][3]
                    trigger = j[1][4]
                    argument = j[1][5]
                    attr_type = j[1][6]
                    target = j[1][7]
                    attribute = j[1][8]
                    annotation_type = j[1][9]
                    (
                        corpus,
                        scenario,
                        event_entry,
                        tokenized_message_index,
                    ) = self.parse_restitution_id(annotation_id)
                    annotation_event = self.get_event_by_parsed_id(
                        corpus, scenario, event_entry, tokenized_message_index
                    )
                    self.add_annotation_to_document_by_dimension(
                        text,
                        span,
                        pos,
                        annotation_event,
                        dimension,
                        trigger,
                        argument,
                        attr_type,
                        target,
                        attribute,
                        annotation_type,
                    )

    def add_annotation_to_document_by_dimension(
        self,
        text,
        span,
        pos,
        annotation_event,
        dimension,
        trigger,
        argument,
        attr_type,
        target,
        attribute,
        annotation_type,
    ):
        argument_id = None
        document = annotation_event.documents_by_dimension[dimension]
        if annotation_type == MammutAnnotations.ANNOTATION_ENTITY_TYPE:
            tuple_span = tuple([int(i) for i in span.split(",")])
            self.mammut_id_brat_id_dict[
                annotation_event.get_id_from_brat_entity(tuple_span, pos)
            ] = document.ann_obj.get_new_id("T")
            annotation = TextBoundAnnotationWithText(
                [tuple_span],
                self.mammut_id_brat_id_dict[
                    annotation_event.get_id_from_brat_entity(tuple_span, pos)
                ],
                pos,
                text,
            )
            document.ann_obj.add_annotation(annotation)
        elif annotation_type == MammutAnnotations.ANNOTATION_EVENT_TYPE:
            brat_id = document.ann_obj.get_new_id("E")
            entity = document.ann_obj.get_ann_by_id(
                self.mammut_id_brat_id_dict[argument]
            )
            type = entity.type
            annotation = {}
            event_exists = False
            # TODO: no seria mejor crear las listas y hacer el inititlaize en vez de crear la intancia yo
            for i in document.ann_obj.get_events():
                if i.trigger == self.mammut_id_brat_id_dict[trigger]:
                    annotation = i
                    event_exists = True

            if not event_exists:
                self.mammut_id_event_brat_id_dict[trigger] = brat_id
                if argument in self.mammut_id_event_brat_id_dict:
                    argument_id = self.mammut_id_event_brat_id_dict[argument]
                else:
                    argument_id = self.mammut_id_brat_id_dict[argument]
                annotation = EventAnnotation(
                    self.mammut_id_brat_id_dict[trigger], [], brat_id, type, "\t"
                )
                annotation.add_argument(entity.type, argument_id)
                document.ann_obj.add_annotation(annotation)
            else:
                if argument in self.mammut_id_event_brat_id_dict:
                    argument_id = self.mammut_id_event_brat_id_dict[argument]
                else:
                    argument_id = self.mammut_id_brat_id_dict[argument]
                annotation.add_argument(entity.type, argument_id)
        elif annotation_type == MammutAnnotations.ANNOTATION_FEATURE_TYPE:
            brat_id = document.ann_obj.get_new_id("A")
            tail = ""
            if target in self.mammut_id_event_brat_id_dict.keys():
                triger = self.mammut_id_event_brat_id_dict[target]
            else:
                triger = self.mammut_id_brat_id_dict[target]
            annotation = AttributeAnnotation(
                triger, brat_id, attr_type, tail, attribute
            )
            document.ann_obj.add_annotation(annotation)
        annotation_event.is_annotated_dimention[dimension] = True

    def add_restitution_to_anotation_event(
        self, restitution: str, annotation_event: MammutEventAnnotation
    ):
        if annotation_event is None:
            return
        annotation_event.event["original_text"] = (
            restitution + " " + annotation_event.event["original_text"]
        )

    def get_event_by_parsed_id(
        self,
        corpus: str,
        scenario_index: int,
        event_entry_index: int,
        tokenized_message_index: int,
    ):
        for i in self.annotation_event_by_corpus[corpus]:
            if (
                i.event[MammutEventAnnotation.SCENARIO_INDEX_ID] == scenario_index
                and i.event[MammutEventAnnotation.EVENT_ENTRY_INDEX_ID]
                == event_entry_index
                and i.event["tokenized_message_index"] == tokenized_message_index
            ):
                return i

    def parse_restitution_id(self, restitution_id):
        words = restitution_id.split("-")
        corpus = "-".join(words[: len(words) - MammutAnnotations.NO_VARIABLE_ID_PARAMS])
        tokenized_message_index = int(words[-1])
        event_entry = int(words[-2])
        scenario = int(words[-3])
        return corpus, scenario, event_entry, tokenized_message_index

    def get_event_messages(self, corpus):
        for i in self.events_by_corpus:
            if i == corpus.sheet_title:
                return self.events_by_corpus[i]

    def get_annotation_event_messages(self, corpus):
        for i in self.annotation_event_by_corpus:
            if i == corpus.sheet_title:
                return self.annotation_event_by_corpus[i]

    def delete_all_annotations(self, event_annotation):
        for dimension in self.default_annotation_dimensions:
            if (
                self.ranges_by_dimension[dimension][event_annotation.get_id()]["range"]
                is not None
            ):
                (
                    result,
                    num_of_deleted_cells,
                ) = event_annotation.delete_annotation_from_sheet(dimension)
                range = self.package.annotations.ranges_by_dimension[dimension][
                    event_annotation.get_id()
                ]["range"]
                jump = range[1] - range[0]
                self.update_ranges(
                    None, dimension, event_annotation.get_id(), jump, only_delete=True
                )
