#!/user/bin/env python
from app import create_app, db, models, forms

app = create_app()


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, m=models, f=forms)


@app.cli.command()
def example_command():
    """Example command."""
    print("Hello World!!!")


@app.cli.command()
def db_populate():
    """Fill DB by dummy data."""
    from tests.db import populate

    populate()


if __name__ == "__main__":
    app.run()
