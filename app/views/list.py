from flask import Blueprint, render_template
from flask_login import login_required
from app import models as m


list_blueprint = Blueprint("list", __name__)


@list_blueprint.route("/list", methods=["GET"])
@login_required
def user_list():

    users = m.User.query.all()

    return render_template("list.html", users=users, enumerate=enumerate)
