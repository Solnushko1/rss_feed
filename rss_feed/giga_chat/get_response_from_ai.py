from environs import Env

from rss_feed.giga_chat.utils.auth import check_auth
from rss_feed.giga_chat.utils.get_answer import get_answer
from rss_feed.giga_chat.utils.get_token import get_jwt_token

env = Env()
env.read_env()
GIGA_JWT_TOKEN = ""


def get_response_from_ai(user_input: str) -> str:
    """Get response from ai."""
    global GIGA_JWT_TOKEN  # noqa: PLW0603
    if not check_auth(giga_jwt_token=GIGA_JWT_TOKEN):
        GIGA_JWT_TOKEN = get_jwt_token(auth_token=env.str("AUTH_GIGA_CHAT"))
    return get_answer(user_message=user_input, auth_token=GIGA_JWT_TOKEN)
