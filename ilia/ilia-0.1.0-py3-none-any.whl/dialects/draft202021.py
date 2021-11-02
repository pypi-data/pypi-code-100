from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Iterable, Type

from ilia import ctx
from ilia.checkers import (
    is_date,
    is_date_time,
    is_duration,
    is_email,
    is_hostname,
    is_idn_email,
    is_idn_hostname,
    is_ipv4,
    is_ipv6,
    is_iri,
    is_iri_reference,
    is_json_pointer,
    is_regex,
    is_relative_json_pointer,
    is_time,
    is_uri,
    is_uri_reference,
    is_uri_template,
    is_uuid,
)
from ilia.evaluators import (
    AdditionalItems,
    AdditionalProperties,
    AllOf,
    AlwaysFalse,
    AlwaysTrue,
    Annotate,
    AnyOf,
    Cluster,
    Conditional,
    Const,
    ContainmentRules,
    Contains,
    DependentRequired,
    DependentSchemas,
    Else,
    Enum,
    ExclusiveMaximum,
    ExclusiveMinimum,
    Format,
    If,
    ItemsRules,
    MaxContains,
    Maximum,
    MaxItems,
    MaxLength,
    MaxProperties,
    MinContains,
    Minimum,
    MinItems,
    MinLength,
    MinProperties,
    MultipleOf,
    Not,
    OneOf,
    Only,
    Pattern,
    PatternProperties,
    PrefixItems,
    Properties,
    PropertiesRules,
    PropertyNames,
    Required,
    Then,
    TypeValidator,
    UnevaluatedItems,
    UnevaluatedProperties,
    UniqueItems,
)
from ilia.ref import Ref, push_fragments, push_pointer

if TYPE_CHECKING:
    from ilia.evaluators import Evaluate
    from ilia.res import Document, Schema

DIALECT = "https://json-schema.org/draft/2020-12/schema"
FORMATS = {
    "date-time": is_date_time,
    "date": is_date,
    "time": is_time,
    "duration": is_duration,
    "email": is_email,
    "idn-email": is_idn_email,
    "hostname": is_hostname,
    "idn-hostname": is_idn_hostname,
    "ipv4": is_ipv4,
    "ipv6": is_ipv6,
    "uri": is_uri,
    "uri-reference": is_uri_reference,
    "iri": is_iri,
    "iri-reference": is_iri_reference,
    "uuid": is_uuid,
    "uri-template": is_uri_template,
    "json-pointer": is_json_pointer,
    "relative-json-pointer": is_relative_json_pointer,
    "regex": is_regex,
}
Missing = object()


def finalize(doc: Document[dict]):
    from ilia.res import canonical_ref_join, canonical_uri_join

    canonical_uri = None
    anchor = None
    ref = None
    if isinstance(doc.schema, dict):
        canonical_uri = doc.schema.get("$id")
        anchor = doc.schema.get("$anchor")
        ref = doc.schema.get("$ref")
    if canonical_uri and doc.parent and (base := doc.parent.canonical_uri):
        canonical_uri = canonical_uri_join(base, canonical_uri)
    if ref and canonical_uri:
        ref = canonical_ref_join(canonical_uri, ref)
    doc.canonical_uri = canonical_uri
    doc.anchor = anchor
    if ref:
        doc.ref = Ref(ref)


def extract(doc: Document[Schema]) -> Iterable[tuple[Schema, str]]:
    if isinstance(doc.schema, bool):
        return
    for keyword in [
        "not",
        "if",
        "else",
        "then",
        "items",
        "contains",
        "additionalProperties",
        "propertyNames",
        "unevaluatedItems",
        "unevaluatedProperties",
    ]:
        if (schema := doc.schema.get(keyword, Missing)) is not Missing:
            yield schema, push_fragments(doc.relative_location, keyword)
    for keyword in ["allOf", "anyOf", "oneOf", "prefixItems"]:
        for i, schema in enumerate(doc.schema.get(keyword, [])):
            yield schema, push_fragments(doc.relative_location, keyword, i)
    for keyword in ["$defs", "dependentSchemas", "properties", "patternProperties"]:
        for key, schema in doc.schema.get(keyword, {}).items():
            yield schema, push_fragments(doc.relative_location, keyword, key)


def compile_schema(doc: Document[dict | bool]) -> Evaluate:
    if doc.schema is True:
        return AlwaysTrue(
            relative_location=ctx.relative_location,
            absolute_keyword_location=doc.absolute_location,
        )
    elif doc.schema is False:
        return AlwaysFalse(
            relative_location=ctx.relative_location,
            absolute_keyword_location=doc.absolute_location,
        )
    else:
        keywords = list(doc.schema)

        unevaluated_items = find_unevaluated_items(doc, keywords)
        unevaluated_props = find_unevaluated_properties(doc, keywords)

        evaluators: list[Evaluate] = []
        evaluators += yield_ref(doc, keywords)
        evaluators += yield_not(doc, keywords)
        evaluators += compile_conditional(doc, keywords)
        evaluators += yield_all_of(doc, keywords)
        evaluators += yield_any_of(doc, keywords)
        evaluators += yield_one_of(doc, keywords)
        evaluators += yield_object(doc, keywords)
        evaluators += yield_array(doc, keywords)
        evaluators += yield_string(doc, keywords)
        evaluators += yield_number(doc, keywords)
        evaluators += yield_type(doc, keywords)
        evaluators += yield_enum(doc, keywords)
        evaluators += yield_const(doc, keywords)
        evaluators += yield_format(doc, keywords)
        evaluators += yield_annotations(doc, keywords)

        return Cluster(
            evaluators=evaluators,
            unevaluated_items=unevaluated_items,
            unevaluated_props=unevaluated_props,
            relative_location=ctx.relative_location,
            absolute_keyword_location=doc.absolute_location,
        )


def find_simple_evaluator(
    doc: Document, keywords: list[str], attr: str, cls: Type[Evaluate]
):
    if sub := ctx.find(doc, attr):
        with ctx.push_relative_location(attr):
            keywords.remove(attr)
            return cls(
                ctx.compile_schema(sub),
                relative_location=ctx.relative_location,
                absolute_keyword_location=sub.absolute_location,
            )


def yield_simple_evaluator(
    doc: Document, keywords: list[str], attr: str, cls: Type[Evaluate]
):
    if evaluator := find_simple_evaluator(doc, keywords, attr, cls):
        yield evaluator


def find_simple_validator(
    doc: Document, keywords: list[str], attr: str, cls: Type[Evaluate]
):
    if (limit := doc.schema.get(attr, Missing)) is not Missing:
        with ctx.push_relative_location(attr):
            keywords.remove(attr)
            return cls(
                limit,
                relative_location=ctx.relative_location,
                absolute_keyword_location=push_pointer(doc.absolute_location, attr),
            )


def yield_simple_validator(
    doc: Document, keywords: list[str], attr: str, cls: Type[Evaluate]
):
    if evaluator := find_simple_validator(doc, keywords, attr=attr, cls=cls):
        yield evaluator


yield_not = partial(yield_simple_evaluator, attr="not", cls=Not)


def compile_conditional(doc: Document, keywords: list[str]):
    when_true = find_then(doc, keywords=keywords)
    when_false = find_else(doc, keywords=keywords)
    if condition := find_if(doc, keywords=keywords):
        yield Conditional(
            condition=condition, when_false=when_false, when_true=when_true
        )


find_if = partial(find_simple_evaluator, attr="if", cls=If)


find_then = partial(find_simple_evaluator, attr="then", cls=Then)


find_else = partial(find_simple_evaluator, attr="else", cls=Else)


@ctx.push_relative_location("$ref")
def yield_ref(doc: Document, keywords: list[str]):
    if sub := doc.ref_doc:
        keywords.remove("$ref")
        yield ctx.compile_schema(sub)


@ctx.push_relative_location("anyOf")
def yield_any_of(doc: Document, keywords: list[str]):
    if docs := ctx.find_sequence(doc, "anyOf"):
        keywords.remove("anyOf")

        yield AnyOf(
            compile_sequence(docs),
            relative_location=ctx.relative_location,
            absolute_keyword_location=push_pointer(doc.absolute_location, "anyOf"),
        )


@ctx.push_relative_location("allOf")
def yield_all_of(doc: Document, keywords: list[str]):
    if docs := ctx.find_sequence(doc, "allOf"):
        keywords.remove("allOf")

        yield AllOf(
            compile_sequence(docs),
            relative_location=ctx.relative_location,
            absolute_keyword_location=push_pointer(doc.absolute_location, "allOf"),
        )


@ctx.push_relative_location("oneOf")
def yield_one_of(doc: Document, keywords: list[str]):
    if docs := ctx.find_sequence(doc, "oneOf"):
        keywords.remove("oneOf")

        yield OneOf(
            compile_sequence(docs),
            relative_location=ctx.relative_location,
            absolute_keyword_location=push_pointer(doc.absolute_location, "oneOf"),
        )


def yield_annotations(doc: Document, keywords: list[str]):
    for keyword in keywords:
        value = doc.schema.get(keyword)
        yield Annotate(
            value=value,
            relative_location=push_fragments(ctx.relative_location, keyword),
            absolute_keyword_location=push_pointer(doc.absolute_location, keyword),
        )
    keywords.clear()


def yield_object(doc: Document, keywords: list[str]):
    evaluators: list[Evaluate] = []
    evaluators += yield_properties_rules(doc, keywords)
    evaluators += yield_property_names(doc, keywords)
    evaluators += yield_dependent_schemas(doc, keywords)
    evaluators += yield_min_properties(doc, keywords)
    evaluators += yield_max_properties(doc, keywords)
    evaluators += yield_required(doc, keywords)
    evaluators += yield_dependent_required(doc, keywords)
    if evaluators:
        yield Only(evaluators=evaluators, type="object")


def yield_properties_rules(doc: Document, keywords: list[str]):
    props = find_props(doc, keywords)
    pattern_props = find_pattern_props(doc, keywords)
    additional_props = find_additional_props(doc, keywords)
    if props or pattern_props or additional_props:
        yield PropertiesRules(
            props=props, pattern_props=pattern_props, additional_props=additional_props
        )


def compile_sequence(docs: list[tuple[int, Document]]) -> list[Evaluate]:
    evaluators = []
    for index, sub in docs:
        with ctx.push_relative_location(index):
            evaluators.append(ctx.compile_schema(sub))
    return evaluators


def compile_mapping(docs: list[tuple[str, Document]]) -> dict[str, Evaluate]:
    evaluators = {}
    for name, sub in docs:
        with ctx.push_relative_location(name):
            evaluators[name] = ctx.compile_schema(sub)
    return evaluators


@ctx.push_relative_location("properties")
def find_props(doc: Document, keywords: list[str]):
    if docs := ctx.find_mapping(doc, "properties"):
        keywords.remove("properties")
        return Properties(
            compile_mapping(docs),
            relative_location=ctx.relative_location,
            absolute_keyword_location=push_pointer(doc.absolute_location, "properties"),
        )


@ctx.push_relative_location("patternProperties")
def find_pattern_props(doc: Document, keywords: list[str]):
    if docs := ctx.find_mapping(doc, "patternProperties"):
        keywords.remove("patternProperties")
        return PatternProperties(
            compile_mapping(docs),
            relative_location=ctx.relative_location,
            absolute_keyword_location=push_pointer(
                doc.absolute_location, "patternProperties"
            ),
        )


find_additional_props = partial(
    find_simple_evaluator, attr="additionalProperties", cls=AdditionalProperties
)


yield_property_names = partial(
    yield_simple_evaluator, attr="propertyNames", cls=PropertyNames
)


@ctx.push_relative_location("dependentSchemas")
def yield_dependent_schemas(doc: Document, keywords: list[str]):
    if docs := ctx.find_mapping(doc, "dependentSchemas"):
        keywords.remove("dependentSchemas")
        yield DependentSchemas(
            compile_mapping(docs),
            relative_location=ctx.relative_location,
            absolute_keyword_location=push_pointer(
                doc.absolute_location, "dependentSchemas"
            ),
        )


yield_min_properties = partial(
    yield_simple_validator, attr="minProperties", cls=MinProperties
)


yield_max_properties = partial(
    yield_simple_validator, attr="maxProperties", cls=MaxProperties
)


yield_required = partial(yield_simple_validator, attr="required", cls=Required)


yield_dependent_required = partial(
    yield_simple_validator, attr="dependentRequired", cls=DependentRequired
)


def yield_array(doc: Document, keywords: list[str]):
    evaluators: list[Evaluate] = []
    evaluators += yield_items_rules(doc, keywords)
    evaluators += yield_containment(doc, keywords)
    evaluators += yield_max_items(doc, keywords)
    evaluators += yield_min_items(doc, keywords)
    evaluators += yield_unique_items(doc, keywords)
    if evaluators:
        yield Only(evaluators=evaluators, type="array")


def yield_items_rules(doc: Document, keywords: list[str]):
    prefix_items = find_prefix_items(doc, keywords)
    additional_items = find_additional_items(doc, keywords)
    if prefix_items or additional_items:
        yield ItemsRules(prefix_items=prefix_items, additional_items=additional_items)


@ctx.push_relative_location("prefixItems")
def find_prefix_items(doc: Document, keywords: list[str]):
    if docs := ctx.find_sequence(doc, "prefixItems"):
        keywords.remove("prefixItems")
        evaluators: list[Evaluate] = []
        for index, sub in docs:
            with ctx.push_relative_location(index):
                evaluators.append(ctx.compile_schema(sub))
        return PrefixItems(
            evaluators,
            relative_location=ctx.relative_location,
            absolute_keyword_location=push_pointer(
                doc.absolute_location, "prefixItems"
            ),
        )


find_additional_items = partial(
    find_simple_evaluator, attr="items", cls=AdditionalItems
)

yield_min_items = partial(yield_simple_validator, attr="minItems", cls=MinItems)


yield_max_items = partial(yield_simple_validator, attr="maxItems", cls=MaxItems)
yield_unique_items = partial(
    yield_simple_validator, attr="uniqueItems", cls=UniqueItems
)


def yield_containment(doc: Document, keywords: list[str]):
    maximum = find_max_contains(doc, keywords)
    minimum = find_min_contains(doc, keywords)
    if contains := find_contains(doc, keywords):
        yield ContainmentRules(contains=contains, minimum=minimum, maximum=maximum)


find_contains = partial(find_simple_evaluator, attr="contains", cls=Contains)


find_max_contains = partial(find_simple_validator, attr="maxContains", cls=MaxContains)


find_min_contains = partial(find_simple_validator, attr="minContains", cls=MinContains)


def yield_string(doc: Document, keywords: list[str]):
    evaluators: list[Evaluate] = []
    evaluators += yield_pattern(doc, keywords)
    evaluators += yield_min_length(doc, keywords)
    evaluators += yield_max_length(doc, keywords)
    if evaluators:
        yield Only(evaluators=evaluators, type="string")


yield_pattern = partial(yield_simple_validator, attr="pattern", cls=Pattern)


yield_min_length = partial(yield_simple_validator, attr="minLength", cls=MinLength)


yield_max_length = partial(yield_simple_validator, attr="maxLength", cls=MaxLength)


def yield_number(doc: Document, keywords: list[str]):
    evaluators: list[Evaluate] = []
    evaluators += yield_minimum(doc, keywords)
    evaluators += yield_maximum(doc, keywords)
    evaluators += yield_exclusive_minimum(doc, keywords)
    evaluators += yield_exclusive_maximum(doc, keywords)
    evaluators += yield_multiple_of(doc, keywords)
    if evaluators:
        yield Only(evaluators=evaluators, type="number")


yield_multiple_of = partial(yield_simple_validator, attr="multipleOf", cls=MultipleOf)


yield_minimum = partial(yield_simple_validator, attr="minimum", cls=Minimum)


yield_maximum = partial(yield_simple_validator, attr="maximum", cls=Maximum)


yield_exclusive_minimum = partial(
    yield_simple_validator, attr="exclusiveMinimum", cls=ExclusiveMinimum
)


yield_exclusive_maximum = partial(
    yield_simple_validator, attr="exclusiveMaximum", cls=ExclusiveMaximum
)


@ctx.push_relative_location("type")
def yield_type(doc: Document, keywords: list[str]):
    if (value := doc.schema.get("type", Missing)) is not Missing:
        keywords.remove("type")
        yield TypeValidator(
            value if isinstance(value, list) else [value],
            relative_location=ctx.relative_location,
            absolute_keyword_location=push_pointer(doc.absolute_location, "type"),
        )


@ctx.push_relative_location("enum")
def yield_enum(doc: Document, keywords: list[str]):
    if (values := doc.schema.get("enum", Missing)) is not Missing:
        keywords.remove("enum")
        yield Enum(
            values,
            relative_location=ctx.relative_location,
            absolute_keyword_location=push_pointer(doc.absolute_location, "enum"),
        )


@ctx.push_relative_location("const")
def yield_const(doc: Document, keywords: list[str]):
    if (value := doc.schema.get("const", Missing)) is not Missing:
        keywords.remove("const")
        yield Const(
            value,
            relative_location=ctx.relative_location,
            absolute_keyword_location=push_pointer(doc.absolute_location, "const"),
        )


def yield_format(doc: Document, keywords: list[str]):
    if (value := doc.schema.get("format", Missing)) is not Missing:
        with ctx.push_relative_location("format"):
            keywords.remove("format")
            checker = ctx.formats.get(value) or FORMATS[value]
            yield Format(
                checker,
                relative_location=ctx.relative_location,
                absolute_keyword_location=push_pointer(doc.absolute_location, "format"),
            )


find_unevaluated_items = partial(
    find_simple_evaluator, attr="unevaluatedItems", cls=UnevaluatedItems
)


find_unevaluated_properties = partial(
    find_simple_evaluator, attr="unevaluatedProperties", cls=UnevaluatedProperties
)
