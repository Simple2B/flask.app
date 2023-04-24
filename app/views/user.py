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

from app import models as m, db
from app import forms as f
from app.logger import log


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/", methods=["GET"])
@login_required
def get_all():
    q = request.args.get("q", type=str, default=None)
    users = m.User.query.order_by(m.User.id)
    if q:
        users = users.filter(m.User.username.like(f"{q}%") | m.User.email.like(f"{q}%"))

    pagination = create_pagination(total=users.count())

    return render_template(
        "user/users.html",
        users=users.paginate(page=pagination.page, per_page=pagination.per_page),
        page=pagination,
        form=f.NewUserForm(),
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
        return redirect(url_for("user.get_all"))


@bp.route("/create", methods=["POST"])
@login_required
def create():
    form = f.NewUserForm()
    if form.validate_on_submit():
        user = m.User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            activated=form.activated.data,
        )
        log(log.INFO, "Form submitted. User: [%s]", user)
        flash("User added!", "success")
        user.save()
        return redirect(url_for("user.get_all"))
    else:
        log(log.ERROR, "User save errors: [%s]", form.errors)
        flash(f"Form is not valid! {form.errors}", "danger")
        return redirect(url_for("user.get_all"))


@bp.route("/delete/<id>", methods=["DELETE"])
@login_required
def delete(id):
    u = m.User.query.filter_by(id=id).first()
    if not u:
        log(log.INFO, "There is no user with id: [%s]", id)
        flash("There is no such user", "danger")
        return "no user", 404

    db.session.delete(u)
    db.session.commit()
    log(log.INFO, "User deleted. User: [%s]", u)
    flash("User deleted!", "success")
    return "ok", 200
