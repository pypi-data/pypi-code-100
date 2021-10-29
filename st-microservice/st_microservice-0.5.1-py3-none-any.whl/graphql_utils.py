from typing import List, Any
from datetime import date

from graphql import GraphQLError
from graphql.type.definition import GraphQLObjectType, get_named_type
from ariadne.types import GraphQLResolveInfo
from sqlalchemy import select, String, Integer, SmallInteger, Numeric, Boolean, Date
from sqlalchemy.orm import Session
from pyparsing import ParseException

from .starlettebackend import User
from .filter_parser import number_filter_parser


nulldate = date(1753, 1, 1)


def parse_date(datep, fieldname: str = 'Date'):
    try:
        return date.fromisoformat(datep)
    except ValueError:
        raise GraphQLError(f'{fieldname} does not have correct format (YYYY-MM-DD)')


def get_dbsession(info) -> Session:
    return info.context['request'].state.dbsession


def get_user(info: GraphQLResolveInfo) -> User:
    return info.context['request'].user


def get_all_records(info, q):
    return get_dbsession(info).execute(q).scalars().unique().all()  # Todo: Watch out for that .unique()


def get_one_record(info, q):
    return get_dbsession(info).execute(q).scalars().first()


def get_one_field(info, q):
    return get_dbsession(info).execute(q).scalar()


def simple_table_resolver_factory(model, query_modifiers=None):
    def simple_table_resolver(_, info, filters: List[Any], limit: int, offset: int):
        q = select(model)

        for f in filters:
            field = getattr(model, f['field_name'])
            field_type = field.type.python_type
            value = f['value']

            # Deducing filter type by model column type. Contrary to resolve_type_inspector.
            try:
                if field_type is str:
                    q = q.where(field.like(value))
                elif field_type is int or field_type is float:
                    q = number_filter_parser(q, field, value)
                elif field_type is date:
                    q = q.where(field == value)
                elif field_type is bool:
                    q = q.where(field == value)
                else:
                    raise GraphQLError(f'Cannot filter on column type {field_type}')
            except ParseException as e:
                raise GraphQLError(f'Cannot parse value: {value} for field {field} of type {field_type} [{e}]')

        if query_modifiers is not None:
            q = query_modifiers(q)

        q = q.limit(limit).offset(offset)

        return get_all_records(info, q)
    return simple_table_resolver


def resolve_type_inspector(_, info: GraphQLResolveInfo, type_name):
    gqltype = info.schema.get_type(type_name)
    if gqltype is None or not isinstance(gqltype, GraphQLObjectType):
        return None

    field_details = []

    all_filter = hasattr(gqltype, '__all_filter__')

    for field_name, field in gqltype.fields.items():
        has_filter = False
        if hasattr(field, '__filter__'):
            if getattr(field, '__filter__'):
                has_filter = True
        elif all_filter:
            has_filter = True

        field_filter_type = None
        if has_filter:
            field_type = get_named_type(field.type)
            if field_type is None:
                raise Exception('Can only filter on Named Types')
            # Deducing Filter type by GraphQL type. Contrary to simple_table_resolver
            if field_type.name == 'String':
                field_filter_type = 'STRING'
            elif field_type.name in ['Int', 'Float']:
                field_filter_type = 'NUMBER'
            else:
                raise GraphQLError(f'Type {field_type.name} cannot support filtering on field {field_name}')

        # Todo: impelement editable
        field_details.append({'field_name': field_name, 'filter_type': field_filter_type, 'editable': False})

    return {'field_details': field_details}
