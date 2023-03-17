from flask_mail import Message
from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app.models import User
from app.forms import LoginForm, RegistrationForm
from app import mail
from config import BaseConfig as conf

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        user.save()

        # create e-mail message
        msg = Message(
            subject="New password",
            sender=conf.MAIL_DEFAULT_SENDER,
            recipients=[user.email],
        )
        url = url_for(
            "auth.activate",
            reset_password_uid=user.unique_id,
            _external=True,
        )

        msg.html = render_template(
            "email/confirm.htm",
            user=user,
            url=url,
            config=conf,
        )
        mail.send(msg)

        login_user(user)
        flash(
            "Registration successful. Checkout you email for confirmation!.", "success"
        )
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("auth/register.html", form=form)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.authenticate(form.user_id.data, form.password.data)
        if user is not None:
            login_user(user)
            flash("Login successful.", "success")
            return redirect(url_for("main.index"))
        flash("Wrong user ID or password.", "danger")
    return render_template("auth/login.html", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "info")
    return redirect(url_for("main.index"))


@auth_blueprint.route("/activated/<reset_password_uid>")
@login_required
def activate(reset_password_uid):
    if not current_user.is_authenticated:
        return redirect(url_for("main.index"))

    user: User = User.query.filter(User.unique_id == reset_password_uid).first()
    user.activated = True
    user.save()

    if not user:
        flash("Incorrect reset password link", "danger")
        return redirect(url_for("main.index"))

    flash("Welcome!", "success")
    return redirect(url_for("main.index"))
