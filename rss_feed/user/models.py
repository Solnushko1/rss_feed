"""User models."""

import datetime as dt
from typing import Any

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from rss_feed.database import Column, PkModel, db, reference_col, relationship
from rss_feed.extensions import bcrypt


class Role(PkModel):
    """A role for a user."""

    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col("users", nullable=True)
    user = relationship("User", backref="roles")

    def __init__(self, name: str, **kwargs: Any) -> None:
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self) -> str:
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"


class User(UserMixin, PkModel):
    """A user of the app."""

    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    _password = Column("password", db.LargeBinary(128), nullable=True)
    created_at = Column(
        db.DateTime,
        nullable=False,
        default=dt.datetime.now(dt.UTC),
    )
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    @hybrid_property
    def password(self):
        """Hashed password."""
        return self._password

    @password.setter  # type:ignore[no-redef]
    def password(self, value: str) -> None:
        """Set password."""
        self._password = bcrypt.generate_password_hash(value)

    def check_password(self, value: str) -> bool:
        """Check password."""
        return bcrypt.check_password_hash(self._password, value)

    @property
    def full_name(self) -> str:
        """Full user name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"
