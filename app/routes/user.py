"""Ping CRM users management routes."""

import os
from datetime import datetime
from io import BytesIO
from typing import Dict
from uuid import uuid4

from flask import Blueprint, current_app, flash, redirect, request, url_for
from flask_inertia import render_inertia
from flask_login import login_required
from marshmallow import EXCLUDE, ValidationError

from app import db
from app.models.account import Account
from app.models.user import User
from app.routes import build_search_data, get_search_filters
from app.serializers import user_schema, users_schema

user_routes = Blueprint("users", __name__)


def save_media(files: Dict[str, BytesIO]) -> str:
    file_ = request.files["photo"]
    ext = file_.filename.split(".")[-1]
    filename = f"{uuid4().hex}.{ext}"
    file_.save(os.path.join(current_app.config["MEDIA_DIR"], filename))
    return url_for("media", filename=filename)


@user_routes.route("/")
@login_required
def search():
    page, name_filter, trash_filter = get_search_filters()
    owner_filter = request.args.get("role")
    query = User.query.filter(User.last_name.ilike(f"%{name_filter}%"))

    if trash_filter == "only":
        query = query.filter(User.deleted_at != None)  # noqa: E711
    elif trash_filter == "":
        query = query.filter(User.deleted_at == None)  # noqa: E711

    if owner_filter is not None:
        arg = owner_filter == "owner"
        query = query.filter(User.owner == arg)

    query = query.order_by(User.id).paginate(
        page, per_page=current_app.config["ITEMS_PER_PAGE"]
    )
    data = build_search_data(
        query, "users", "users.search", name_filter, trash_filter, users_schema
    )
    return render_inertia("users/Search", props=data)


@user_routes.route("/create/", methods=["GET", "POST"])
@login_required
def create():
    errors = {}
    data = {}
    if request.method == "POST":
        request_data = dict(request.form)

        try:
            pwd = request_data.pop("password", None)
            if pwd is None:
                raise ValidationError({"password": "This field is required"})

            user = user_schema.load(request_data)
            user.set_password(pwd)
            account = Account(name=f"{user.last_name} {user.first_name}")
            user.account = account

            if "photo" in request.files:
                photo_path = save_media(request.files)
                user.photo_path = photo_path

            db.session.add(account)
            db.session.add(user)
            db.session.commit()
            data["user"] = user_schema.dump(user)
            flash("User created.", "success")
        except ValidationError as err:
            errors = err.normalized_messages()
            flash("There is one form error.", "error")

    data["errors"] = errors
    return render_inertia("users/Create", props=data)


@user_routes.route("/<user_id>/edit/", methods=["GET", "PUT"])
@login_required
def edit(user_id: int):
    errors = {}
    user = User.query.get_or_404(user_id)
    if request.method == "PUT":
        request_data = dict(request.form)
        try:
            pwd = request_data.pop("password", None)
            user_schema.load(request_data, partial=True, unknown=EXCLUDE)
            request_data["owner"] = request_data.get("owner", 0) == 1
            user.update(request_data)

            if pwd:
                user.set_password(pwd)

            if "photo" in request.files:
                photo_path = save_media(request.files)
                user.photo_path = photo_path

            db.session.commit()
            flash("User updated.", "success")
        except ValidationError as err:
            errors = err.normalized_messages()
            flash("There is one form error.", "error")

    data = {
        "errors": errors,
        "mode": "edit",
        "user": user_schema.dump(user),
    }
    return render_inertia("users/Edit", props=data)


@user_routes.route("/<user_id>/delete/", methods=["DELETE"])
@login_required
def delete(user_id: int):
    user = User.query.get_or_404(user_id)
    user.deleted_at = datetime.now()
    db.session.commit()
    flash("User deleted.", "success")
    return redirect(url_for("users.edit", user_id=user_id))


@user_routes.route("/<user_id>/restore/", methods=["PUT"])
@login_required
def restore(user_id: int):
    user = User.query.get_or_404(user_id)
    user.deleted_at = None
    db.session.commit()
    flash("User restored.", "success")
    return redirect(url_for("users.edit", user_id=user_id))
