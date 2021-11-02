from typing import List

from .model import AttributeValuePair, Entity, EncoderRequest, AttributeSchema, EncoderConfig, EncodedEntity


def serialize_attribute_value_pair(pair: AttributeValuePair, include_type=False) -> dict:
    """
    Converts an attribute value pair into a dictionary:

    :param pair: Attribute value pair to convert
    :param include_type: ``True`` if the value's data type should be included, ``False`` otherwise
    :return: Converted attribute value pair
    """
    d = {
        "name": pair.name,
        "value": pair.value_as_string()
    }

    if include_type:
        d["data-type"] = pair.resolve_data_type()

    return d


def serialize_attribute_value_pairs(pair_list: List[AttributeValuePair], include_type=False) -> List[dict]:
    """
    Converts a list of attribute value pairs into a list of dictionaries.

    :param pair_list: List of attribute value pairs to convert
    :param include_type: ``True`` if the data type for every attribute value pair should be included,
    ``False`` otherwise
    :return: List of converted attribute value pairs
    """
    return [
        serialize_attribute_value_pair(pair, include_type) for pair in pair_list
    ]


def serialize_entity(entity: Entity, include_type=False) -> dict:
    """
    Converts an entity into a dictionary.

    :param entity: Entity to convert
    :param include_type: ``True`` if the data type should be included for each of the entity's attributes,
    ``False`` otherwise
    :return: Converted entity
    """
    return {
        "identifier": entity.identifier,
        "attribute-value-list": serialize_attribute_value_pairs(entity.attributes, include_type)
    }


def serialize_entities(entity_list: List[Entity], include_type=False) -> List[dict]:
    """
    Converts an list of entities into a list of dictionaries.

    :param entity_list: Entities to convert
    :param include_type: ``True`` if the data type should be included for each of the entities' attributes,
    ``False`` otherwise
    :return: List of converted entities
    """
    return [
        serialize_entity(entity, include_type) for entity in entity_list
    ]


def serialize_schema(schema: AttributeSchema) -> dict:
    """
    Converts an attribute schema into a dictionary.

    :param schema: Attribute schema to convert
    :return: Converted attribute schema
    """
    d = {"attribute-name": schema.attribute_name}
    d.update({
        k: str(v) for k, v in schema.options.items()
    })

    return d


def serialize_schemas(schema_list: List[AttributeSchema]) -> List[dict]:
    """
    Converts a list of attribute schemas into a dictionary.

    :param schema_list: Attribute schemas to convert
    :return: List of converted attribute schemas
    """
    return [
        serialize_schema(schema) for schema in schema_list
    ]


def serialize_encoder_config(config: EncoderConfig) -> dict:
    """
    Converts an encoder configuration object into a dictionary.

    :param config: Encoder configuration to convert
    :return: Converted encoder configuration
    """
    return {
        "charset": config.charset,
        "seed": config.seed,
        "generation-function": config.generation_function
    }


def serialize_encoder_request(request: EncoderRequest, force_include_schema=False) -> dict:
    """
    Converts an encoder request object into a dictionary.

    :param request: Encoder request to convert
    :param force_include_schema: ``True`` if attribute schemas should be generated regardless of whether any have been
    supplied in the request object, ``False`` otherwise
    :return: Converted encoder request
    """
    if len(request.entity_list) == 0:
        raise ValueError("Entity list must contain at least one entity")

    should_include_schema = len(request.schema_list) != 0 or force_include_schema

    d = serialize_encoder_config(request.config)
    d["entity-list"] = serialize_entities(request.entity_list, include_type=not should_include_schema)

    # if the schema is present, we need an extra field. otherwise we're done.
    if not should_include_schema:
        return d

    # map attribute names to serialized schemas for easy lookup later
    attr_to_schema_mapping: dict[str, dict] = {
        schema.attribute_name: serialize_schema(schema) for schema in request.schema_list
    }

    schema_list: List[dict] = []
    first_entity = request.entity_list[0]

    # use first entity as a reference
    for attr in first_entity.attributes:
        schema = {
            "attribute-name": attr.name,
            "data-type": attr.resolve_data_type()
        }

        # check if there exists a schema for this attribute and merge the schema definition with
        # the present data type
        other_schema = attr_to_schema_mapping.get(attr.name)

        if other_schema is not None:
            schema.update(other_schema)

        schema_list.append(schema)

    d["schema-list"] = schema_list
    return d


def deserialize_encoded_entity(d: dict) -> EncodedEntity:
    """
    Converts a dictionary into an encoded entity.

    :param d: Dictionary to convert
    :return: Converted dictionary
    """
    return EncodedEntity(d["identifier"], d["encoding"])
