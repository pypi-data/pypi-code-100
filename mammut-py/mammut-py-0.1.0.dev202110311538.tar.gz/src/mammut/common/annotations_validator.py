# coding=utf-8
from mammut.common.lexicon.pos import POSType
from brat_widget.document import *
import copy


class Parents:
    def __init__(self, depth, parents=None):
        self.parents = parents
        self.depth = depth

    def get(self):
        if self.parents is not None:
            return self.parents


class Overlap:
    def __init__(self, overlap_type):
        self.overlap_type = overlap_type


class Entity:
    def __init__(self, entity, parents=None):
        self.entity = entity  # objeto annotation
        self.parents = parents


# permitimos que entities overlap pueda expresar los solapamientos de los entities y tmabien los solapamientos de eventos, simplemente sabemos que los
# entites de eventos solapados son iguales
# convierte el evento solapado e un objeto entitiesoverlap
class EventEntitesOverlap:
    def __init__(self, entity, parents):
        self.entites_overlap = EntitiesOverlap()
        self.entity_original = Entity(entity, parents)
        self.entites_overlap.add(self.entity_original)
        self.entity_copy = Entity(entity, parents)
        self.entites_overlap.add(self.entity_copy)

    def get_entities_overlap(self):
        return self.enties_overlap


class EntitiesOverlap:
    def __init__(self):
        self.entities_list = list()

    def add(self, entity):
        self.entities_list.append(entity)


class EventAnnotationValidator:
    def __init__(self, package, annotation):
        self.package = package
        self.annotation = annotation
        self.valid = True
        self.invalid_type = list()  # event_list y/o entity listy
        self.annotation_lists_by_dimension = dict()
        self.sorted_annotations_list_by_dimension = dict()
        self.valid_sets_by_dimention = dict()
        self.invalid_spans_pairs_by_dimension = dict()
        self.event_annotation_by_dimension = dict()
        self.all_enties_with_overlaped_parents_by_dimension = dict()
        self.overlaped_enties_parents_by_dimension = dict()
        self.has_nested_overlaps = False

        for dimension in self.annotation.documents_by_dimension:
            self.sorted_annotations_list_by_dimension[dimension] = dict()
            self.valid_sets_by_dimention[dimension] = dict()
            self.annotation_lists_by_dimension[dimension] = dict()
            self.annotation_lists_by_dimension[dimension][
                EventsAnnotationsValidator.ENTITIES_LIST
            ] = list()
            self.annotation_lists_by_dimension[dimension][
                EventsAnnotationsValidator.EVENTS_LIST
            ] = list()
            self.event_annotation_by_dimension[dimension] = list()

        self.get_entities_and_events_lists()
        self.sort_and_validate()

    def get_entities_and_events_lists(self):
        for dimension in self.annotation.documents_by_dimension:
            for i in self.annotation.documents_by_dimension[
                dimension
            ].ann_obj.get_textbounds():
                # TODO:no se incluyen las preposiciones, i.type no es un key de descriptor_list
                if i.type in self.package.standard.pos_descriptor_list:
                    if (
                        self.package.standard.pos_descriptor_list[i.type].pos_type
                        != POSType.Event
                    ):
                        self.annotation_lists_by_dimension[dimension][
                            EventsAnnotationsValidator.ENTITIES_LIST
                        ].append(i)
                    else:
                        self.annotation_lists_by_dimension[dimension][
                            EventsAnnotationsValidator.EVENTS_LIST
                        ].append(i)
            for i in self.annotation.documents_by_dimension[
                dimension
            ].ann_obj.get_events():
                self.event_annotation_by_dimension[dimension].append(i)

    # recibe lista de textboundanotations
    # TODO:list_type es indica si es entity o event_list, de ser event list creo que no tiene utilidad
    def is_valid_subset(self, sorted_list, dimension, list_type):
        valid = True
        for i, elem in enumerate(sorted_list[:-1]):
            a = sorted_list[i].spans[0]
            b = sorted_list[i + 1].spans[0]
            seta = set(range(a[0], a[1] + 1))
            setb = set(range(b[0], b[1] + 1))
            # print(valid, seta, setb, seta-setb, setb-seta)
            if dimension not in self.invalid_spans_pairs_by_dimension.keys():
                self.invalid_spans_pairs_by_dimension[dimension] = dict()
            if list_type not in self.invalid_spans_pairs_by_dimension[dimension].keys():
                self.invalid_spans_pairs_by_dimension[dimension][list_type] = list()
            if len(seta & setb) > 1 and len(seta - setb) > 0 and len(setb - seta) > 0:
                invalid_tuple = tuple([sorted_list[i], sorted_list[i + 1]])
                self.invalid_spans_pairs_by_dimension[dimension][list_type].append(
                    invalid_tuple
                )
                valid = False
                # break
        return valid

    def get_nested_overlaped_events(self):
        overlaped_spans = list()
        overlaps_by_dimension = self.all_enties_with_overlaped_parents_by_dimension
        # entity = ovrelap
        for dimension, overlap in overlaps_by_dimension.items():
            if len(overlap):
                overlaped_spans.append(
                    (
                        overlap[0].entities_list[0].entity.text,
                        self.annotation.event["original_text"],
                        dimension,
                    )
                )
        return overlaped_spans

    def get_parents(self, span, dimension):
        # print(span.type, 'de quien obtenemos los padres')
        parents = list()
        # TODO: no deberia incluir este metodo tambien alas entidades solapadas?overlaped_enties_parents_by_dimension
        for event in self.annotation.documents_by_dimension[
            dimension
        ].ann_obj.get_events():
            # TODO:deberia ser en funcion del texto o del id??con el texto se obtienen overlaps raros
            # if span.type in [arg[0] for arg in event.args]:
            if span.id in [arg[1] for arg in event.args]:
                parents.append(
                    self.annotation.documents_by_dimension[
                        dimension
                    ].ann_obj.get_ann_by_id(event.trigger)
                )
        if len(parents):
            for i in parents:
                self.get_parents(i, dimension)
        return parents

    def get_events_arguments(self, dimension):
        # calculamos los padres de todos los spans
        parents = None
        if dimension not in self.all_enties_with_overlaped_parents_by_dimension.keys():
            self.all_enties_with_overlaped_parents_by_dimension[dimension] = list()
        if dimension not in self.overlaped_enties_parents_by_dimension.keys():
            self.overlaped_enties_parents_by_dimension[dimension] = list()
        for entity in self.sorted_annotations_list_by_dimension[dimension][
            EventsAnnotationsValidator.ENTITIES_LIST
        ]:
            parents = self.get_parents(entity, dimension)
            # print('*************')
            if len(parents) >= 2:
                self.has_nested_overlaps = True
                self.all_enties_with_overlaped_parents_by_dimension[dimension].append(
                    EventEntitesOverlap(entity, parents).entites_overlap
                )
                self.valid = False
                # TODO:revisar esto de invalid type, puede ser invalido en varios types
                if EventsAnnotationsValidator.EVENTS_LIST not in self.invalid_type:
                    self.invalid_type.append(EventsAnnotationsValidator.EVENTS_LIST)
                # TODO: si esto pasa marcamos el evento como solpado/invalido??
                # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
                # print(parents)
        # si hay overlap de entities en capa1 obtenemos los padres de los solapados
        # y sabemos que los padres son eventos solapados
        if dimension in self.invalid_spans_pairs_by_dimension.keys():
            if (
                EventsAnnotationsValidator.ENTITIES_LIST
                in self.invalid_spans_pairs_by_dimension[dimension].keys()
            ):
                # si entra en este fi es poruqe son entities con solapamiento por eso marcamos como invalidos e indicamos quienes son los parents
                for overlaped_arguments in self.invalid_spans_pairs_by_dimension[
                    dimension
                ][EventsAnnotationsValidator.ENTITIES_LIST]:
                    parents = None
                    parents_list = list()
                    enties_overlap = EntitiesOverlap()
                    for argument in overlaped_arguments:
                        print("##### when entie overlap")
                        parents = self.get_parents(argument, dimension)
                        parents_list = parents_list + parents
                        enties_overlap.add(Entity(argument, parents))
                    # TODO: duplicare algo de la data de all_enties_with_overlaped_parents_by_dimension?
                    if len(parents_list) >= 2:
                        self.overlaped_enties_parents_by_dimension[dimension].append(
                            enties_overlap
                        )
                        self.has_nested_overlaps = True
                        self.valid = False
                        if (
                            EventsAnnotationsValidator.EVENTS_LIST
                            not in self.invalid_type
                        ):
                            self.invalid_type.append(
                                EventsAnnotationsValidator.EVENTS_LIST
                            )
                        print("overlaped events")

    def sort_and_validate(self):
        for dimension in self.sorted_annotations_list_by_dimension:
            # print(dimension)
            self.sorted_annotations_list_by_dimension[dimension][
                EventsAnnotationsValidator.ENTITIES_LIST
            ] = self.bubble_sort(
                self.annotation_lists_by_dimension[dimension][
                    EventsAnnotationsValidator.ENTITIES_LIST
                ]
            )
            self.sorted_annotations_list_by_dimension[dimension][
                EventsAnnotationsValidator.EVENTS_LIST
            ] = self.bubble_sort(
                self.annotation_lists_by_dimension[dimension][
                    EventsAnnotationsValidator.EVENTS_LIST
                ]
            )
            self.valid_sets_by_dimention[dimension][
                EventsAnnotationsValidator.ENTITIES_LIST
            ] = self.is_valid_subset(
                self.sorted_annotations_list_by_dimension[dimension][
                    EventsAnnotationsValidator.ENTITIES_LIST
                ],
                dimension,
                EventsAnnotationsValidator.ENTITIES_LIST,
            )
            # TODO: esta validacion de entities de eventos solapados no aporta informacion valiosa???
            self.valid_sets_by_dimention[dimension][
                EventsAnnotationsValidator.EVENTS_LIST
            ] = self.is_valid_subset(
                self.sorted_annotations_list_by_dimension[dimension][
                    EventsAnnotationsValidator.EVENTS_LIST
                ],
                dimension,
                EventsAnnotationsValidator.EVENTS_LIST,
            )
            # NOTE: despues de validar si es invalido como se hacian antes, ahora validamos contran los argumentos de los eventos
            self.get_events_arguments(dimension)  # TODO:esto puede ir e otro metodo??
        for dimension in self.valid_sets_by_dimention:
            for key, val in self.valid_sets_by_dimention[dimension].items():
                if not val:  # un valor falso, que e slo mismo que un set invalido
                    self.valid = False
                    # print(key)
                    if key not in self.invalid_type:
                        self.invalid_type.append(key)
                        # break

    def contains(self, tupA, tupB):
        # print('a en b', tupA, tupB, tupA[0] >= tupB[0] and tupA[1]<=tupB[1])
        return tupA[0] >= tupB[0] and tupA[1] <= tupB[1]

    def bubble_sort(self, array):
        # print('#########################\nunsorted\n', [i.spans[0] for i in array])
        index = len(array) - 1
        while index >= 0:
            for j in range(index):
                # A = array[j]
                # B = array[j+1]
                # print('pair', array[j].spans[0], array[j+1].spans[0])
                if (
                    array[j].spans[0][0] > array[j + 1].spans[0][0]
                ):  # comparacion de primer numero de la tupla
                    if not self.contains(array[j].spans[0], array[j + 1].spans[0]):
                        array[j], array[j + 1] = array[j + 1], array[j]
                elif array[j].spans[0][0] < array[j + 1].spans[0][0]:
                    if self.contains(array[j + 1].spans[0], array[j].spans[0]):
                        array[j], array[j + 1] = array[j + 1], array[j]
                elif array[j].spans[0][0] == array[j + 1].spans[0][0]:
                    if self.contains(
                        array[j + 1].spans[0], array[j].spans[0]
                    ):  # segundo elemento contenido enel primero?
                        # if not contains(array[j], array[j+1]):#primer elemento contenido enel segundo?
                        array[j], array[j + 1] = array[j + 1], array[j]
                        # print([i.spans[0] for i in array])

            index -= 1
        # print('\nsorted\n', [i.spans[0] for i in array])
        return array

    # esto computa casi lo mismo que is_valid_subset
    def get_overlap_spans(self, sorted_list):
        overlap_pairs = list()
        valid = True
        for i, elem in enumerate(sorted_list[:-1]):
            a = sorted_list[i].spans[0]
            b = sorted_list[i + 1].spans[0]
            seta = set(range(a[0], a[1] + 1))
            setb = set(range(b[0], b[1] + 1))
            # print(valid, seta, setb, seta-setb, setb-seta)
            # print(valid, seta, setb, seta-setb, setb-seta)
            if seta & setb and len(seta - setb) > 0 and len(seta - setb) > 0:
                # overlap_pairs.append(sorted_list[i].type +'-'+ sorted_list[i+1].type)
                overlap_pairs.append((sorted_list[i], sorted_list[i + 1]))
        return overlap_pairs


class EventsAnnotationsValidator:
    ENTITIES_LIST = "entities_list"
    EVENTS_LIST = "events_list"

    def __init__(self, corpus, package):
        self.package = package
        self.event_annotation_validator_list = list()
        self.invalid_events = list()
        self.valid_events = list()
        self.invalid_by_dimension = dict()
        self.invalid_annotations_pairs_count = dict()
        self.overlap_spans_list = list()

        for event_ann in self.package.annotations.annotation_event_by_corpus[
            corpus.sheet_title
        ]:
            eavalidator = EventAnnotationValidator(self.package, event_ann)
            self.event_annotation_validator_list.append(eavalidator)
            if eavalidator.valid:
                self.valid_events.append(eavalidator)
            else:
                self.invalid_events.append(eavalidator)
            for dimension in eavalidator.valid_sets_by_dimention:
                # invalidos por dimension
                if dimension not in self.invalid_by_dimension.keys():
                    self.invalid_by_dimension[dimension] = {}
                if (
                    EventsAnnotationsValidator.EVENTS_LIST
                    not in self.invalid_by_dimension[dimension].keys()
                ):
                    self.invalid_by_dimension[dimension][
                        EventsAnnotationsValidator.EVENTS_LIST
                    ] = list()
                if (
                    EventsAnnotationsValidator.ENTITIES_LIST
                    not in self.invalid_by_dimension[dimension].keys()
                ):
                    self.invalid_by_dimension[dimension][
                        EventsAnnotationsValidator.ENTITIES_LIST
                    ] = list()
                # se toman en cuenta eventos para analisis
                if eavalidator.has_nested_overlaps:
                    # solo aqi porque son de tipo event_list
                    self.invalid_by_dimension[dimension][
                        EventsAnnotationsValidator.EVENTS_LIST
                    ] = (
                        self.invalid_by_dimension[dimension][
                            EventsAnnotationsValidator.EVENTS_LIST
                        ]
                        + eavalidator.all_enties_with_overlaped_parents_by_dimension[
                            dimension
                        ]
                    )
                # se toman en cuenta los entities para analisis
                if not eavalidator.valid_sets_by_dimention[dimension][
                    EventsAnnotationsValidator.ENTITIES_LIST
                ]:
                    overlap_pairs = eavalidator.get_overlap_spans(
                        eavalidator.sorted_annotations_list_by_dimension[dimension][
                            EventsAnnotationsValidator.ENTITIES_LIST
                        ]
                    )
                    enties_overlap = EntitiesOverlap()
                    for pair in overlap_pairs:
                        for entity_annotation in pair:
                            enties_overlap.add(Entity(entity_annotation))
                    self.invalid_by_dimension[dimension][
                        EventsAnnotationsValidator.ENTITIES_LIST
                    ].append(enties_overlap)
                    overlap_span_values = (
                        overlap_pairs[0][1].spans[0][0],
                        overlap_pairs[0][0].spans[0][1],
                    )
                    self.overlap_spans_list.append(
                        (
                            eavalidator.annotation.event["original_text"][
                                overlap_span_values[0] : overlap_span_values[1]
                            ],
                            eavalidator.annotation.event["original_text"],
                            dimension,
                        )
                    )
            if eavalidator.has_nested_overlaps:
                self.overlap_spans_list = (
                    self.overlap_spans_list + eavalidator.get_nested_overlaped_events()
                )

        for (
            key,
            dimension_values,
        ) in self.invalid_by_dimension.items():  # echange, {event_list:[],entitlist:[]}
            for list_type, list_element in dimension_values.items():
                for entitie_overlap in list_element:
                    ann_pair_text = (
                        entitie_overlap.entities_list[0].entity.type
                        + "-"
                        + entitie_overlap.entities_list[1].entity.type
                    )
                    if ann_pair_text not in self.invalid_annotations_pairs_count:
                        self.invalid_annotations_pairs_count[ann_pair_text] = dict()
                        self.invalid_annotations_pairs_count[ann_pair_text] = 1
                    else:
                        self.invalid_annotations_pairs_count[ann_pair_text] += 1

    def get_annotation_params_copy(self, annotation, dimension):
        params = dict()
        params["text_bounds"] = list()
        for i in annotation.documents_by_dimension[dimension].ann_obj.get_textbounds():
            params["text_bounds"].append(i)
        params["events"] = list()
        for i in annotation.documents_by_dimension[dimension].ann_obj.get_events():
            params["events"].append(i)
        params["attributes"] = list()
        for i in annotation.documents_by_dimension[dimension].ann_obj.get_attributes():
            params["attributes"].append(i)
        return params

    def restore_from_params(self, annotation, dimension, params):
        annotation.initialize_configuration(dimension)
        annotation.initialize_document(dimension, annotation.event)
        document = annotation.documents_by_dimension[dimension]
        for text_bound in params["text_bounds"]:
            document.ann_obj.add_annotation(text_bound)
        for event in params["events"]:
            document.ann_obj.add_annotation(event)
        for attributes in params["attributes"]:
            document.ann_obj.add_annotation(attributes)

    def visualize_overlap_from_event_validator(
        self, ann_obj_validator, selected_dimension
    ):
        visualizers_list = list()
        for dimension, dim_vals in ann_obj_validator.valid_sets_by_dimention.items():
            # print(dimension, dim_vals, '<<<<<<<<<<<<<<<<<<<<<<<>>>>>>')
            for type_list, elem_type in dim_vals.items():
                if False == elem_type and dimension == selected_dimension:
                    params_copy = self.get_annotation_params_copy(
                        ann_obj_validator.annotation, dimension
                    )
                    # print('dibujamos data de ', type_list, dimension)
                    ann_obj_validator.annotation.initialize_configuration(dimension)
                    ann_obj_validator.annotation.initialize_document(
                        dimension, ann_obj_validator.annotation.event
                    )
                    document = ann_obj_validator.annotation.documents_by_dimension[
                        dimension
                    ]
                    overlap_pairs = ann_obj_validator.get_overlap_spans(
                        ann_obj_validator.sorted_annotations_list_by_dimension[
                            dimension
                        ][type_list]
                    )
                    # print(overlap_pairs)
                    for i in overlap_pairs[0]:
                        # print(i)
                        annotation = TextBoundAnnotationWithText(
                            i.spans, i.id, i.type, i.text
                        )
                        # print('overlap_pair', annotation)
                        document.ann_obj.add_annotation(annotation)
                    visualizers_list.append(
                        ann_obj_validator.annotation.get_visualizer(dimension, None)
                    )
                    self.restore_from_params(
                        ann_obj_validator.annotation, dimension, params_copy
                    )
        return visualizers_list

    def get_event_appearance(self, ann_obj_validator, elem_type):
        count = 0
        annotation_events = [
            i.annotation for i in self.invalid_events + self.valid_events
        ]
        for index, event_ann in enumerate(annotation_events):
            for dimension in event_ann.documents_by_dimension:
                for i in event_ann.documents_by_dimension[
                    dimension
                ].ann_obj.get_textbounds():
                    if i.type == elem_type:
                        count += 1
        return count

    def get_event_overlap_and_overall_count(self, ann_obj_validator):
        overlap_pair_type_count = dict()
        overlap_pair_type = None
        for (
            dimension
        ) in (
            self.invalid_by_dimension
        ):  # cualquier dict que tenga los key de dimensiones
            for invalid_type in ann_obj_validator.invalid_type:
                overlap_pairs = ann_obj_validator.get_overlap_spans(
                    ann_obj_validator.sorted_annotations_list_by_dimension[dimension][
                        invalid_type
                    ]
                )
                if len(overlap_pairs):
                    overlap_pair_type = (
                        overlap_pairs[0][0].type + "-" + overlap_pairs[0][1].type
                    )
                    for overlap_pair in overlap_pairs:
                        appearance_count = dict()
                        for i in overlap_pair:
                            appearance_count[i.type] = self.get_event_appearance(
                                ann_obj_validator, i.type
                            )
                            overlap_pair_type_count[
                                overlap_pair_type
                            ] = appearance_count
        return overlap_pair_type_count


class CorpusAnnotationsValidator:
    def __init__(self, package):
        self.annotations_validator_by_corpus = dict()
        for corpus in package.corpus_map.get_all_corpus():
            if corpus.annotable:
                annotations_validator = EventsAnnotationsValidator(corpus, package)
                self.annotations_validator_by_corpus[
                    corpus.sheet_title
                ] = annotations_validator
