# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from datetime import datetime
from mongoengine import Document, fields
from pymongo import ASCENDING


class ReviewDocument(Document):
    """A mapping object to convert MongoDB data to a Review object."""

    meta = {
        "indexes": [
            {"name": "review_title", "fields": ["title"]},
        ],
        "db_alias": "default",
        "collection": "reviews",
        "strict": False,
    }

    # basic properties
    title = fields.StringField(min_length=1, max_length=100, required=True)
    text = fields.StringField(min_length=1, max_length=4000, required=True)

    # relations
    volume = fields.StringField(required=True)
    tags = fields.ListField(field=fields.ReferenceField("TagDocument"))

    # audit properties
    created_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    created_by = fields.StringField(default="system", required=True)
    updated_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    updated_by = fields.StringField(default="system", required=True)
    deleted_at = fields.DateTimeField(null=True)
    deleted_by = fields.StringField(default="system", required=True)
