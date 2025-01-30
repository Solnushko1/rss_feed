from typing import Any

from sqlalchemy.exc import SQLAlchemyError

from rss_feed.extensions import db
from rss_feed.post.model import Post


def delete_all_posts_from_db() -> None:
    try:
        for post in Post.query.all():
            db.session.delete(post)
    except SQLAlchemyError:
        db.session.rollback()
    else:
        db.session.commit()


def save_posts_to_db(data: dict[str, Any]) -> None:
    try:
        Post.create(
            name=data["name"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            short_description=data["short_description"],
            link=data["link"],
        )
    except SQLAlchemyError:
        db.session.rollback()
    else:
        db.session.commit()
