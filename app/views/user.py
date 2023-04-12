from flask import Blueprint, render_template, request
from flask_login import login_required
from app.controllers import create_pagination

from app import models as m


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/", methods=["GET"])
@login_required
def get_all():
    q = request.args.get("q", type=str, default=None)
    users = m.User.query
    if q:
        users.filter(m.User.username.like(f"{q}%") | m.User.email.like(f"{q}%"))

    pagination = create_pagination(total=users.count())

    return render_template(
        "users.html",
        users=users.paginate(page=pagination.page, per_page=pagination.per_page),
        page=pagination,
    )
