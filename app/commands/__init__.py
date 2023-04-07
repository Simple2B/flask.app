import click
from flask import Flask
from app import models as m
from app import db, forms
from app.logger import log


def init(app: Flask):

    # flask cli context setup
    @app.shell_context_processor
    def get_context():
        """Objects exposed here will be automatically available from the shell."""
        return dict(app=app, db=db, m=m, f=forms)

    @app.cli.command()
    def example_command():
        """Example command."""
        print("Hello World!!!")

    @app.cli.command()
    @click.option("--count", default=100, type=int)
    def db_populate(count: int):
        """Fill DB by dummy data."""
        if app.config["ENV"] == "production":
            log(
                log.WARNING, "This command does not working in production configuration"
            )
            return
        from tests.db import populate

        populate(count)
        print(f"DB populated by {count} instancies")

    @app.cli.command("create-admin")
    def create_admin():
        """Create super admin account"""
        if m.User.query.filter_by(email=app.config["ADMIN_EMAIL"]).first():
            print(f"User with e-mail: [{app.config['ADMIN_EMAIL']}] already exists")
            return
        m.User(
            username=app.config["ADMIN_USERNAME"],
            email=app.config["ADMIN_EMAIL"],
            password=app.config["ADMIN_PASSWORD"],
        ).save()
        print("admin created")
