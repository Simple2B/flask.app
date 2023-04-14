from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from flask_login import login_required
from app.controllers import create_pagination

from app import models as m
from app import forms as f
from app.logger import log


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/", methods=["GET"])
@login_required
def get_all():
    q = request.args.get("q", type=str, default=None)
    users = m.User.query.order_by(m.User.id)
    if q:
        users.filter(m.User.username.like(f"{q}%") | m.User.email.like(f"{q}%"))

    pagination = create_pagination(total=users.count())

    return render_template(
        "users.html",
        users=users.paginate(page=pagination.page, per_page=pagination.per_page),
        page=pagination,
    )


@bp.route("/save", methods=["POST"])
@login_required
def save():
    form = f.UserForm()
    if form.validate_on_submit():
        u: m.User = m.User.query.get(int(form.user_id.data))
        if not u:
            log(log.ERROR, "Not found user by id : [%s]", form.user_id.data)
            flash("Cannot save user data", "danger")
        u.username = form.username.data
        u.email = form.email.data
        u.activated = form.activated.data
        if form.password.data.strip("*\n "):
            u.password = form.password.data
        u.save()
        if form.next_url.data:
            return redirect(form.next_url.data)
        return redirect(url_for("user.get_all"))

    else:
        log(log.ERROR, "User save errors: [%s]", form.errors)
        flash(f"{form.errors}", "danger")
        # return status_code = 40?
        # return Response(jsonify(form.errors), status=400)
        return redirect(url_for("user.get_all"))
