from flask import Blueprint, render_template, request
from flask import current_app as app
from flask_login import login_required
from flask_paginate import Pagination, get_page_parameter

from app import models as m


list_blueprint = Blueprint("list", __name__)


@list_blueprint.route("/list", methods=["GET"])
@login_required
def user_list():
    search = False
    q = request.args.get("q")
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)

    users = m.User.query
    pagination = Pagination(
        page=page,
        total=users.count(),
        search=search,
        record_name="users",
        per_page=app.config["DEFAULT_PAGE_SIZE"],
    )
    # 'page' is the default name of the page parameter, it can be customized
    # e.g. Pagination(page_parameter='p', ...)
    # or set PAGE_PARAMETER in config file
    # also likes page_parameter, you can customize for per_page_parameter
    # you can set PER_PAGE_PARAMETER in config file
    # e.g. Pagination(per_page_parameter='pp')

    return render_template(
        "list.html",
        users=users.paginate(page=page, per_page=app.config["DEFAULT_PAGE_SIZE"]),
        pagination=pagination,
    )
