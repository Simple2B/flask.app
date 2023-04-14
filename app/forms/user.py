from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    ValidationError,
    BooleanField,
)
from wtforms.validators import DataRequired, Email, Length, EqualTo

from app import models as m


class UserForm(FlaskForm):
    next_url = StringField("next_url")
    user_id = StringField("user_id", [DataRequired()])
    email = StringField("email", [DataRequired(), Email()])
    activated = BooleanField("activated")
    username = StringField("Username", [DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 30)])
    password_confirmation = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Password do not match."),
        ],
    )
    submit = SubmitField("Save")

    def validate_username(self, field):
        if (
            m.User.query.filter_by(username=field.data)
            .filter(m.User.id != int(self.user_id.data))
            .first()
            is not None
        ):
            raise ValidationError("This username is taken.")

    def validate_email(self, field):
        if (
            m.User.query.filter_by(email=field.data)
            .filter(m.User.id != int(self.user_id.data))
            .first()
            is not None
        ):
            raise ValidationError("This email is already registered.")


class NewUserForm(FlaskForm):
    email = StringField("email", [DataRequired(), Email()])
    activated = BooleanField("activated")
    username = StringField("Username", [DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 30)])
    password_confirmation = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Password do not match."),
        ],
    )
    submit = SubmitField("Save")

    def validate_username(self, field):
        if m.User.query.filter_by(username=field.data).first() is not None:
            raise ValidationError("This username is taken.")

    def validate_email(self, field):
        if m.User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError("This email is already registered.")
