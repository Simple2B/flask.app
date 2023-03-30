import os
from functools import lru_cache
from pydantic import BaseSettings
from flask import Flask

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_ENV = os.environ.get("APP_ENV", "development")


class BaseConfig(BaseSettings):
    """Base configuration."""

    ENV: str = "base"
    APP_NAME: str = "Simple Flask App"
    SECRET_KEY: str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    WTF_CSRF_ENABLED: bool = False

    # Mail config
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USE_TLS: bool
    MAIL_USE_SSL: bool
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_DEFAULT_SENDER: str

    @staticmethod
    def configure(app: Flask):
        # Implement this method to do further configuration on your app.
        pass

    class Config:
        # `.env` takes priority over `project.env`
        env_file = "project.env", ".env"


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///" + os.path.join(
        BASE_DIR, "database-dev.sqlite3"
    )

    class Config:
        fields = {
            "SQLALCHEMY_DATABASE_URI": {
                "env": "DEVEL_DATABASE_URL",
            }
        }


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING: bool = True
    PRESERVE_CONTEXT_ON_EXCEPTION: bool = False
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///" + os.path.join(
        BASE_DIR, "database-test.sqlite3"
    )

    class Config:
        fields = {
            "SQLALCHEMY_DATABASE_URI": {
                "env": "TEST_DATABASE_URL",
            }
        }


class ProductionConfig(BaseConfig):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "database.sqlite3")
    )
    WTF_CSRF_ENABLED = True

    class Config:
        fields = {
            "SQLALCHEMY_DATABASE_URI": {
                "env": "DATABASE_URL",
            }
        }


@lru_cache
def config(name=APP_ENV) -> DevelopmentConfig | TestingConfig | ProductionConfig:
    CONF_MAP = dict(
        development=DevelopmentConfig(),
        testing=TestingConfig(),
        production=ProductionConfig(),
    )
    configuration = CONF_MAP[name]
    configuration.ENV = name
    return configuration
