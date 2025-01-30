import feedparser
import requests

from rss_feed.post.utils.actions_with_db import delete_all_posts_from_db, save_posts_to_db
from rss_feed.post.utils.validaters import validate_date, validate_text


class RssReader:
    """Class for creating RSS Reader."""

    def __init__(self, rss_url: str) -> None:
        self.rss_url = rss_url

    def fetch_entries(self) -> list[dict[str, str]]:
        """Считывает записи из RSS-ленты."""
        response = requests.get(self.rss_url, verify=False, timeout=3)  # noqa: S501
        feed = feedparser.parse(response.content)
        return feed.entries


def prepare_data_for_db() -> None:
    """Function that prepares data for db"""

    rss_url = "https://www.google.ru/alerts/feeds/11383541103172355775/5490122602639252907"
    rss_reader = RssReader(rss_url)
    delete_all_posts_from_db()
    entries = rss_reader.fetch_entries()
    for entry in entries:
        news_item = {
            "name": validate_text(text=entry.get("title", "")),
            "short_description": validate_text(text=entry.get("summary", "")),  # type: ignore[attr-defined]
            "link": entry.get("link", ""),
            "created_at": validate_date(input_date=entry.get("published", "")),
            "updated_at": validate_date(input_date=entry.get("updated", "")),
        }
        save_posts_to_db(data=news_item)
