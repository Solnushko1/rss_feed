"""Database unit tests."""

from typing import TYPE_CHECKING

import pytest
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.orm.exc import ObjectDeletedError

from rss_feed.database import Column, PkModel, db

if TYPE_CHECKING:
    from rss_feed.user.models import User


class ExampleUserModel(UserMixin, PkModel):
    """Example model class for a user."""

    __tablename__ = "testusers"
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)

    def __init__(self, username: str, email: str) -> None:
        """Create instance."""
        super().__init__(username=username, email=email)


@pytest.mark.usefixtures("db")
class TestCRUDMixin:
    """CRUDMixin tests."""

    def test_create(self) -> None:
        """Test CRUD create."""
        user: User = ExampleUserModel.create(username="foo", email="foo@bar.com")
        user_db = ExampleUserModel.get_by_id(record_id=user.id)
        assert user_db is not None
        assert user_db.username == "foo"

    def test_create_save(self) -> None:
        """Test CRUD create with save."""
        user = ExampleUserModel(username="foo", email="foo@bar.com")
        user.save()
        assert ExampleUserModel.get_by_id(user.id) is not None

    def test_delete_with_commit(self) -> None:
        """Test CRUD delete with commit."""
        user = ExampleUserModel(username="foo", email="foo@bar.com")
        user.save()
        user.delete(commit=True)
        assert ExampleUserModel.get_by_id(user.id) is None

    def test_delete_without_commit_cannot_access(self) -> None:
        """Test CRUD delete without commit."""
        user = ExampleUserModel(username="foo", email="foo@bar.com")
        user.save()
        user.delete(commit=False)
        with pytest.raises(ObjectDeletedError):
            ExampleUserModel.get_by_id(user.id)

    @pytest.mark.parametrize(("commit", "expected"), [(True, "bar"), (False, "foo")])
    def test_update(
        self,
        *,
        commit: bool,
        expected: str,
        db: SQLAlchemy,
    ) -> None:
        """Test CRUD update with and without commit."""
        user = ExampleUserModel(username="foo", email="foo@bar.com")
        user.save()
        user.update(commit=commit, username="bar")
        query = text("select * from testusers")
        retrieved = db.session.execute(query).fetchone()
        assert retrieved is not None
        assert retrieved.username == expected


class TestPkModel:
    """PkModel tests."""

    def test_get_by_id_wrong_type(self) -> None:
        """Test get_by_id returns None for non-numeric argument."""
        assert ExampleUserModel.get_by_id("xyz") is None
