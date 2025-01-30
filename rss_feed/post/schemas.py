from marshmallow import Schema, fields
from marshmallow.fields import DateTime, Integer, String


class BasePostSchema(Schema):
    """Basic layout for Posts."""

    id: Integer = fields.Int()
    name: String = fields.Str()
    created_at: DateTime = fields.DateTime()
    updated_at: DateTime = fields.DateTime()
    short_description: String = fields.Str()


class CreatePostSchema(BasePostSchema):
    """Scheme for creating posts."""

    content = fields.Str()


class DetailPostSchema(CreatePostSchema):
    """Schema for getting detail of post."""


class ListPostSchema(BasePostSchema):
    """Scheme for getting posts."""
