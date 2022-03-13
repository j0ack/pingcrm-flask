"""Ping CRM app test config."""

import os

SECRET_KEY = "test"
LOGIN_DISABLED = True
SQLALCHEMY_DATABASE_URI = (
    f"sqlite:////{os.path.abspath(os.path.dirname(__file__))}/test_db.db"
)
INERTIA_TEMPLATE = "base.html"
ITEMS_PER_PAGE = 10
MEDIA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "media")
