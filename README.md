# Simple Flask App

1. Run

```bash
poetry install
```

2. Create '.env' file (simply copy file .env.sample):

3. Run

```bash
docker compose up d db
```

to create an docker container

4. Development and debugging

   This project contains both Flask and FastAPI.

   To run Flask app:

   - go to "Run and Debug" tab in VSCode and select "Python:Flask" from dropdown menu

   To run FastAPI app:

   - go to "Run and Debug" tab in VSCode and select "API" from dropdown menu

   After selection, press `"Run and Debug"` button or `F5` key on keyboard

5. Create db with command

```bash
flask db upgrade
```

6. In main folder need install node_modules to work with tailwind, run

```bash
yarn
```
