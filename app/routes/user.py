"""Ping CRM users management routes."""

import os
from datetime import datetime
from uuid import uuid4

from flask import Blueprint, current_app, flash, redirect, request, url_for
from flask_inertia import render_inertia
from flask_login import login_required

from app import db
from app.models.account import Account
from app.models.user import User
from app.routes import build_search_data, get_search_filters

user_routes = Blueprint("users", __name__)


@user_routes.route("/")
@login_required
def search():
    page, name_filter, trash_filter = get_search_filters()
    owner_filter = request.args.get("role")
    query = User.query.filter(User.last_name.ilike(f"%{name_filter}%"))

    if trash_filter == "only":
        query = query.filter(User.deleted_at == None)  # noqa: E711
    elif trash_filter is None:
        query = query.filter(User.deleted_at != None)  # noqa: E711

    if owner_filter is not None:
        arg = owner_filter == "owner"
        query = query.filter(User.owner == arg)

    query = query.order_by(User.id).paginate(
        page, per_page=current_app.config["ITEMS_PER_PAGE"]
    )
    data = build_search_data(
        query, "users", "users.search", name_filter, trash_filter
    )
    return render_inertia("users/Search", props=data)


@user_routes.route("/create/", methods=["GET", "POST"])
@login_required
def create():
    errors = {}
    if request.method == "POST":

        request_data = request.form
        for field in ["last_name", "first_name", "email", "password"]:
            if not request_data.get(field):
                errors[field] = "This field is required."

        if errors:
            for field, msg in errors.items():
                flash(f"Field {field}: {msg}.", "error")
        else:
            user = User(
                first_name=request_data.get("first_name"),
                last_name=request_data.get("last_name"),
                email=request_data.get("email"),
                owner=request_data.get("owner"),
            )
            user.set_password(request_data.get("password"))

            account = Account(name=f"{user.last_name} {user.first_name}")
            user.account = account

            db.session.add(account)
            db.session.add(user)
            db.session.commit()
            flash("User created.", "success")

    return render_inertia("users/Create")


@user_routes.route("/<user_id>/edit/", methods=["GET", "PUT"])
@login_required
def edit(user_id: int):
    errors = {}
    user = User.query.get_or_404(user_id)
    if request.method == "PUT":

        request_data = request.form

        for field in ["last_name", "first_name", "email"]:
            if not request_data.get(field):
                errors[field] = "This field is required."

        if errors:
            flash("There is one form error.", "error")
        else:
            user.first_name = request_data.get("first_name")
            user.last_name = request_data.get("last_name")
            user.email = request_data.get("email")
            user.owner = request_data.get("owner") == "1"

            if pwd := request_data.get("password"):
                user.set_password(pwd)

            if "photo" in request.files:
                file_ = request.files["photo"]
                ext = file_.filename.split(".")[-1]
                filename = f"{uuid4().hex}.{ext}"
                file_.save(os.path.join(current_app.config["MEDIA_DIR"], filename))
                user.photo_path = url_for("media", filename=filename)

            db.session.commit()
            flash("User updated.", "success")

    data = {
        "errors": errors,
        "mode": "edit",
        "user": user.to_dict(),
    }
    return render_inertia("users/Edit", props=data)


@user_routes.route("/<user_id>/delete/", methods=["DELETE"])
@login_required
def delete(user_id: int):
    user = User.query.get_or_404(user_id)
    user.deleted_at = datetime.now()
    db.session.commit()
    flash("User deleted.", "success")
    return redirect(url_for("users.edit", n_id=user_id))


@user_routes.route("/<user_id>/restore/", methods=["PUT"])
@login_required
def restore(user_id: int):
    user = User.query.get_or_404(user_id)
    user.deleted_at = None
    db.session.commit()
    flash("User restored.", "success")
    return redirect(url_for("users.edit", user_id=user_id))
