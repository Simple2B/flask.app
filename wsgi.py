#!/user/bin/env python
from app import create_app
from app import commands

app = create_app()
commands.init(app)

if __name__ == "__main__":
    app.run()
