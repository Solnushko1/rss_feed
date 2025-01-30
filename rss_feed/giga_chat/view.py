from typing import Any

from flask import Blueprint, Response, jsonify, request
from starlette import status

from rss_feed.giga_chat.get_response_from_ai import get_response_from_ai
from rss_feed.post.model import Post

blueprint = Blueprint("giga-chat", __name__, url_prefix="/send-request", static_folder="../static")


@blueprint.route("/", methods=["POST"])
def send_request() -> tuple[dict[str, str], Any] | tuple[Response, Any] | dict[str, str | Any]:
    """The handler of the paraphrase request."""
    data = request.get_json()
    post_id = data.get("post_id")
    user_input = data.get("user_input", "").strip()

    if not post_id:
        return {"error": "post_id is required"}, status.HTTP_400_BAD_REQUEST

    if not (post := Post.query.get(post_id)):
        return jsonify(
            {
                "error": "Post not found",
                "message": f"No post with ID {post_id} exists in the database.",
            },
        ), status.HTTP_404_NOT_FOUND

    if not user_input:
        return {"error": "Введите текст для преобразования!"}, status.HTTP_400_BAD_REQUEST

    rephrased_text = get_response_from_ai(user_input=user_input)

    return {"rephrased_text": rephrased_text, "post_id": post.id}
