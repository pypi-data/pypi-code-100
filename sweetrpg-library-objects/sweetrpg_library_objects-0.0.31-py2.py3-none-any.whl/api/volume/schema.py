# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields
from sweetrpg_library_objects.model.volume import Volume
from sweetrpg_api_core.schema.base import BaseAPISchema


class VolumeAPISchema(BaseAPISchema):
    model_class = Volume

    class Meta:
        type_ = "volume"
        self_view = "volume_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "volume_list"

    name = fields.Str()  # , load_only=True)
    slug = fields.Str()  # , load_only=True)
    system = fields.Str()  # , load_only=True)
    authors = Relationship(
        self_view="volume_authors",
        self_view_kwargs={"id": "<id>"},
        related_view="author_list",
        related_view_kwargs={"volume_id": "<id>"},
        many=True,
        schema="AuthorAPISchema",
        type_="author",
    )
    properties = fields.List(fields.Dict(keys=fields.Str(), values=fields.Str()))
