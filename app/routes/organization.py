"""Ping CRM organizations management routes."""

from datetime import datetime

from flask import Blueprint, current_app, flash, redirect, request, url_for
from flask_inertia import render_inertia
from flask_login import login_required
from marshmallow import ValidationError

from app import db
from app.models.account import Account
from app.models.organization import Organization
from app.routes import build_search_data, get_search_filters
from app.serializers import organization_schema, organizations_schema

organization_routes = Blueprint("organization", __name__)


@organization_routes.route("/")
@login_required
def search():
    page, name_filter, trash_filter = get_search_filters()
    query = Organization.query.filter(Organization.name.ilike(f"%{name_filter}%"))

    if trash_filter == "only":
        query = query.filter(Organization.deleted_at != None)  # noqa: E711
    elif trash_filter == "":
        query = query.filter(Organization.deleted_at == None)  # noqa: E711

    query = query.order_by(Organization.id).paginate(
        page, per_page=current_app.config["ITEMS_PER_PAGE"]
    )
    data = build_search_data(
        query,
        "organizations",
        "organization.search",
        name_filter,
        trash_filter,
        organizations_schema,
    )
    return render_inertia("organizations/Search", props=data)


@organization_routes.route("/create/", methods=["GET", "POST"])
@login_required
def create():
    errors = {}
    data = {}
    if request.method == "POST":
        request_data = request.get_json()
        try:
            organization = organization_schema.load(request_data)
            account = Account(name=organization.name)
            organization.account = account
            db.session.add(account)
            db.session.add(organization)
            db.session.commit()
            data["organization"] = organization_schema.dump(organization)
            flash("Organization created.", "success")
        except ValidationError as err:
            errors = err.normalized_messages()
            flash("There is one form error.", "error")

    data["errors"] = errors
    return render_inertia("organizations/Create", props=data)


@organization_routes.route("/<organization_id>/edit/", methods=["GET", "PUT"])
@login_required
def edit(organization_id: int):
    errors = {}
    organization = Organization.query.get_or_404(organization_id)
    if request.method == "PUT":
        request_data = request.get_json()
        try:
            organization_schema.load(request_data)
            organization.update(request_data)
            db.session.commit()
            flash("Organization updated.", "success")
        except ValidationError as err:
            errors = err.normalized_messages()
            flash("There is one form error.", "error")

    data = {
        "errors": errors,
        "mode": "edit",
        "organization": organization_schema.dump(organization),
    }
    return render_inertia("organizations/Edit", props=data)


@organization_routes.route("/<organization_id>/delete/", methods=["DELETE"])
@login_required
def delete(organization_id: int):
    organization = Organization.query.get_or_404(organization_id)
    organization.deleted_at = datetime.now()
    db.session.commit()
    flash("Organization deleted.", "success")
    return redirect(url_for("organization.edit", organization_id=organization_id))


@organization_routes.route("/<organization_id>/restore/", methods=["PUT"])
@login_required
def restore(organization_id: int):
    organization = Organization.query.get_or_404(organization_id)
    organization.deleted_at = None
    db.session.commit()
    flash("Organization restored.", "success")
    return redirect(url_for("organization.edit", organization_id=organization_id))
