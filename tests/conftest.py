"""Defines fixtures available to all tests."""

import logging
from collections.abc import Generator

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from webtest import TestApp

from rss_feed.app import create_app
from rss_feed.database import db as _db

from .factories import UserFactory


@pytest.fixture
def app() -> Generator[Flask]:
    """Create application for the tests."""
    _app = create_app("tests.settings")
    _app.logger.setLevel(logging.CRITICAL)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def testapp(app: Flask) -> TestApp:
    """Create Webtest app."""
    return TestApp(app)


@pytest.fixture
def db(app: Flask) -> Generator[SQLAlchemy]:
    """Create database for the tests."""
    _db.app = app  # type:ignore[attr-defined]
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def user(db: SQLAlchemy) -> UserFactory:
    """Create user for the tests."""
    user = UserFactory(password="myprecious")  # noqa: S106
    db.session.commit()
    return user
