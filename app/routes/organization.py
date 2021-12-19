"""Ping CRM organizations management routes."""

from datetime import datetime

from flask import Blueprint, current_app, flash, redirect, request, url_for
from flask_inertia import render_inertia
from flask_login import login_required

from app import db
from app.models.organization import Organization
from app.routes import build_search_data, get_search_filters

organization_routes = Blueprint("organization", __name__)


@organization_routes.route("/")
@login_required
def search():
    page, name_filter, trash_filter = get_search_filters()
    query = Organization.query.filter(Organization.name.ilike(f"%{name_filter}%"))

    if trash_filter == "only":
        query = query.filter(Organization.deleted_at == None)  # noqa: E711
    elif trash_filter is None:
        query = query.filter(Organization.deleted_at != None)  # noqa: E711

    query = query.order_by(Organization.id).paginate(
        page, per_page=current_app.config["ITEMS_PER_PAGE"]
    )
    data = build_search_data(
        query, "organizations", "organization.search", name_filter, trash_filter
    )
    return render_inertia("organizations/Search", props=data)


@organization_routes.route("/create/", methods=["GET", "POST"])
@login_required
def create():
    errors = {}
    if request.method == "POST":

        request_data = request.get_json()

        if not request_data.get("name"):
            errors["name"] = "The name field is required."
            flash("There is one form error.", "error")
        else:
            organization = Organization(
                name=request_data.get("name"),
                email=request_data.get("email"),
                phone=request_data.get("phone"),
                city=request_data.get("city"),
                address=request_data.get("address"),
                region=request_data.get("region"),
                country=request_data.get("country"),
                postal_code=request_data.get("postal_code"),
            )
            db.session.add(organization)
            db.sesion.commit()
            flash("Organization created.", "success")

    return render_inertia("organizations/Create")


@organization_routes.route("/<organization_id>/edit/", methods=["GET", "PUT"])
@login_required
def edit(organization_id: int):
    errors = {}
    organization = Organization.query.get_or_404(organization_id)
    if request.method == "PUT":

        request_data = request.get_json()

        if not request_data.get("name"):
            errors["name"] = "The name field is required."
            flash("There is one form error.", "error")
        else:
            organization.name = request_data.get("name")
            organization.email = request_data.get("email")
            organization.phone = request_data.get("phone")
            organization.city = request_data.get("city")
            organization.address = request_data.get("address")
            organization.region = request_data.get("region")
            organization.country = request_data.get("country")
            organization.postal_code = request_data.get("postal_code")
            db.session.commit()
            flash("Organization updated.", "success")

    data = {
        "errors": errors,
        "mode": "edit",
        "organization": organization.to_dict(),
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
