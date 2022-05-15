"""Ping CRM simple app."""

import os
from collections import defaultdict

from flask import Flask, current_app, get_flashed_messages, send_from_directory
from flask_inertia import Inertia, render_inertia
from flask_login import LoginManager, current_user, login_required
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
inertia = Inertia()
login_manager = LoginManager()


@login_required
def dashboard():
    return render_inertia("Dashboard")


@login_required
def media(filename: str):
    return send_from_directory(current_app.config["MEDIA_DIR"], filename)


def flash_messages():
    data = defaultdict(list)
    messages = get_flashed_messages(with_categories=True)
    for category, message in messages:
        data[category].append(message)

    return data


def auth_data():
    user = current_user
    data = {}
    if user.is_authenticated:
        data = {
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "owner": user.owner,
                "account": {
                    "name": user.account.name,
                },
            }
        }
    return data


def create_app(config_filename: str) -> Flask:
    app = Flask(
        __name__,
        template_folder=os.path.join(ROOT_DIR, "templates"),
        static_folder=os.path.join(ROOT_DIR, "static", "dist"),
    )
    app.config.from_pyfile(f"{config_filename}.py")

    db.init_app(app)
    migrate.init_app(
        app,
        db,
        render_as_batch=app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"),
    )
    ma.init_app(app)
    inertia.init_app(app)
    inertia.share("flash", flash_messages)
    inertia.share("auth", auth_data)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    app.add_url_rule("/", "dashboard", dashboard)
    app.add_url_rule("/media/<filename>/", "media", media)

    from app.cli import seed

    app.cli.add_command(seed)

    from app.routes.auth import auth
    from app.routes.contact import contact_routes
    from app.routes.organization import organization_routes
    from app.routes.user import user_routes

    app.register_blueprint(auth)
    app.register_blueprint(organization_routes, url_prefix="/organizations/")
    app.register_blueprint(contact_routes, url_prefix="/contacts/")
    app.register_blueprint(user_routes, url_prefix="/users/")

    return app
