"""Post views."""

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from starlette import status
from werkzeug import Response

from rss_feed.extensions import db
from rss_feed.post.form import CreatePostForm
from rss_feed.post.model import Post
from rss_feed.post.utils.filling_db import prepare_data_for_db
from rss_feed.utils import flash_errors

blueprint = Blueprint("post", __name__, url_prefix="/posts", static_folder="../static")


@blueprint.route("/create", methods=["GET", "POST"])
def create_post() -> Response | str:
    """Create a new post."""
    form = CreatePostForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            new_post: Post = Post.create(
                name=form.name.data,
                short_description=form.short_description.data,
                link="",
            )
            db.session.add(new_post)
            db.session.commit()
            flash("Post created successfully!", "success")
            return redirect(url_for("post.get_posts"))

    else:
        flash_errors(form)
    return render_template("post/create_post.html", form=form)


@blueprint.route("/<int:post_id>", methods=["GET"])
def get_detail_post(post_id: int) -> str | tuple[Response, int]:
    if post := Post.query.get(post_id):
        return render_template("post/get_detail_post.html", post=post)
    return jsonify(
        {
            "error": "Post not found",
            "message": f"No post with ID {post_id} exists in the database.",
        },
    ), status.HTTP_404_NOT_FOUND


@blueprint.route("/", methods=["GET"])
def get_posts() -> str:
    prepare_data_for_db()
    posts = Post.query.all()
    return render_template("post/get_posts.html", posts=posts)
