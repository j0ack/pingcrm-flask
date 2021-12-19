"""Ping CRM app dev config."""

import os

SECRET_KEY = "dev"
SQLALCHEMY_DATABASE_URI = (
    f"sqlite:////{os.path.abspath(os.path.dirname(__file__))}/test.db"
)
INERTIA_TEMPLATE = "base.html"
ITEMS_PER_PAGE = 10
MEDIA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "media")
