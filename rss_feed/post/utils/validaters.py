import re
from datetime import UTC, datetime


def validate_date(input_date: str) -> datetime:
    if len(input_date) < 1:
        return datetime.now(UTC)
    return datetime.strptime(input_date, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def validate_text(text: str) -> str:
    """Validate getting text"""
    return re.sub(
        r"&lt;b&gt;|&lt;/b&gt;|<b>|</b>|&#39;|&amp;#39;|&amp;amp;|&amp;nbsp;|&amp;middot;|&quot;|&nbsp;|&middot;",
        "",
        text,
    )
