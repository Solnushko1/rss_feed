from typing import Any

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class CreatePostForm(FlaskForm):
    """Form for creating a post."""

    name = StringField(
        "Title",
        validators=[DataRequired(), Length(min=3, max=100)],
    )
    short_description = StringField(
        "Short Description",
        validators=[Optional(), Length(max=255)],
    )
    content = TextAreaField(
        "Content",
        validators=[DataRequired(), Length(min=10)],
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the form."""
        super().__init__(*args, **kwargs)
