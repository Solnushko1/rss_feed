"""Helper utilities and decorators."""

from flask import flash
from flask_wtf import FlaskForm


def flash_errors(form: FlaskForm, category: str = "warning") -> None:
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)
