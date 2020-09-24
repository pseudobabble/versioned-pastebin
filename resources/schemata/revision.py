#!/usr/bin/env python

from marshmallow import Schema, fields


class RevisionSchema(Schema):
    id = fields.Integer()
    content = fields.String()
    timestamp = fields.DateTime()
    document_id = fields.Integer()
