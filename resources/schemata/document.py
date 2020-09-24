#!/usr/bin/env python

from marshmallow import Schema, fields

from resources.schemata.revision import RevisionSchema


class DocumentSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    revisions = fields.List(fields.Nested(RevisionSchema))
