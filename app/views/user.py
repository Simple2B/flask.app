from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from flask_login import login_required
import sqlalchemy as sa
from app.controllers import create_pagination

from app import models as m, db
from app import forms as f
from app.logger import log


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/", methods=["GET"])
@login_required
def get_all():
    q = request.args.get("q", type=str, default=None)
    where = m.User.is_deleted.is_(False)
    if q:
        where = sa.and_(where, m.User.username.like(f"{q}%") | m.User.email.like(f"{q}%"))  # type: ignore

    query = sa.select(m.User).where(where).order_by(m.User.id)
    count_query = sa.select(sa.func.count()).select_from(m.User).where(where)
    pagination = create_pagination(total=db.session.scalar(count_query))

    return render_template(
        "user/users.html",
        users=db.session.execute(
            query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
        ).scalars(),
        page=pagination,
        search_query=q,
    )


@bp.route("/get-edit-form/<user_uuid>", methods=["GET"])
@login_required
def get_edit_form(user_uuid: str):
    """htmx request"""
    user: m.User | None = db.session.scalar(m.User.select().where(m.User.uuid == user_uuid))
    if not user or user.is_deleted:
        log(log.ERROR, "User not found by id: [%s]", user_uuid)
        return render_template("toast.html", category="danger", message="User not found"), 404
    form = f.UserForm(
        user_uuid=user.uuid,
        email=user.email,
        username=user.username,
        activated=user.activated,
    )
    return render_template("user/edit_modal.html", form=form)


@bp.route("/save", methods=["POST"])
@login_required
def save():
    form = f.UserForm()
    if form.validate_on_submit():
        query = m.User.select().where(m.User.uuid == form.user_uuid.data)
        user: m.User | None = db.session.scalar(query)
        if not user:
            log(log.ERROR, "Not found user by id : [%s]", form.user_uuid.data)
            flash("Cannot save user data", "danger")
            return redirect(url_for("user.get_all"))
        user.username = form.username.data
        user.email = form.email.data
        user.activated = form.activated.data
        if form.password.data.strip("*\n "):
            user.password = form.password.data
        user.save()
        flash("User updated!", "success")
        if form.next_url.data:
            return redirect(form.next_url.data)
        return redirect(url_for("user.get_all"))

    else:
        log(log.ERROR, "User save errors: [%s]", form.errors)
        flash(f"{form.errors}", "danger")

    return redirect(url_for("user.get_all"))


@bp.route("/get-add-form", methods=["GET"])
@login_required
def get_add_form():
    """htmx request"""
    form = f.NewUserForm()
    return render_template("user/add_modal.html", form=form)


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
    if form.errors:
        log(log.ERROR, "User create errors: [%s]", form.errors)
        flash(f"{form.errors}", "danger")

    return redirect(url_for("user.get_all"))


@bp.route("/delete/<user_uuid>", methods=["DELETE"])
@login_required
def delete(user_uuid: str):
    """htmx request"""
    user = db.session.scalar(sa.select(m.User).where(m.User.uuid == user_uuid))
    if not user or user.is_deleted:
        log(log.INFO, "There is no user with id: [%s]", id)
        return render_template("toast.html", category="danger", message="User not found"), 404

    datetime_now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    user.is_deleted = True
    user.username = f"deleted_{user.username}_at_{datetime_now}"
    user.email = f"deleted_{user.email}_at_{datetime_now}"
    db.session.commit()
    log(log.INFO, "User deleted. User: [%s]", user)
    return render_template("toast.html", category="success", message="User deleted!"), 202
