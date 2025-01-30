"""Model unit tests."""

import datetime as dt

import pytest
from flask_sqlalchemy import SQLAlchemy

from rss_feed.user.models import Role, User

from .factories import UserFactory


@pytest.mark.usefixtures("db")
class TestUser:
    """User tests."""

    def test_get_by_id(self, user: UserFactory) -> None:
        """Get user by ID."""
        user.save()

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self, user: UserFactory) -> None:
        """Test creation date."""
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_password_is_nullable(self) -> None:
        """Test null password."""
        user = UserFactory()
        user.save()
        assert user.password is None

    def test_factory(self, db: SQLAlchemy) -> None:
        """Test user factory."""
        user: User = UserFactory(password="myprecious")  # noqa: S106
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.is_admin is False
        assert user.active is True
        assert user.check_password("myprecious")

    def test_check_password(self) -> None:
        """Check password."""
        user: User = User.create(  # type:ignore[assignment]
            username="foo",
            email="foo@bar.com",
            password="foobarbaz123",  # noqa: S106
        )
        assert user.check_password(value="foobarbaz123") is True
        assert user.check_password(value="barfoobaz") is False

    def test_full_name(self) -> None:
        """User full name."""
        user = UserFactory(first_name="Foo", last_name="Bar")
        assert user.full_name == "Foo Bar"

    def test_roles(self) -> None:
        """Add a role to a user."""
        role = Role(name="admin")
        role.save()
        user = UserFactory()
        user.roles.append(role)
        user.save()
        assert role in user.roles

    def test_roles_repr(self) -> None:
        """Check __repr__ output for Role."""
        role = Role(name="user")
        assert role.__repr__() == "<Role(user)>"

    def test_user_repr(self) -> None:
        """Check __repr__ output for User."""
        user = User(username="foo", email="foo@bar.com")
        assert user.__repr__() == "<User('foo')>"
