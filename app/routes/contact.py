"""Ping CRM contacts management routes."""

from datetime import datetime

from flask import Blueprint, current_app, flash, redirect, request, url_for
from flask_inertia import render_inertia
from flask_login import login_required
from marshmallow import ValidationError

from app import db
from app.models.account import Account
from app.models.contact import Contact
from app.models.organization import Organization
from app.routes import build_search_data, get_search_filters
from app.serializers import contact_schema, contacts_schema, organizations_schema

contact_routes = Blueprint("contacts", __name__)


@contact_routes.route("/")
@login_required
def search():
    page, name_filter, trash_filter = get_search_filters()
    query = Contact.query.filter(Contact.last_name.ilike(f"%{name_filter}"))

    if trash_filter == "only":
        query = query.filter(Contact.deleted_at == None)  # noqa: E711
    elif trash_filter is None:
        query = query.filter(Contact.deleted_at != None)  # noqa: E711

    query = query.order_by(Contact.id).paginate(
        page, per_page=current_app.config["ITEMS_PER_PAGE"]
    )
    data = build_search_data(
        query,
        "contacts",
        "contacts.search",
        name_filter,
        trash_filter,
        contacts_schema,
    )
    return render_inertia("contacts/Search", props=data)


@contact_routes.route("/create/", methods=["GET", "POST"])
@login_required
def create():
    organizations = organizations_schema.dump(
        [org for org in Organization.query.all()]
    )
    errors = {}
    if request.method == "POST":
        request_data = request.get_json()
        try:
            contact = contact_schema.load(request_data)
            account = Account(name=contact.name)
            contact.account = account
            db.session.add(account)
            db.session.add(contact)
            db.session.commit()
            flash("Contact created.", "success")
        except ValidationError as err:
            errors = err.normalized_messages()
            flash("There is one form error.", "error")

    data = {
        "errors": errors,
        "organizations": organizations,
    }

    return render_inertia("contacts/Create", props=data)


@contact_routes.route("/<contact_id>/edit/", methods=["GET", "PUT"])
@login_required
def edit(contact_id: int):
    errors = {}
    organizations = organizations_schema.dump(
        [org for org in Organization.query.all()]
    )
    contact = Contact.query.get_or_404(contact_id)
    if request.method == "PUT":
        request_data = request.get_json()
        try:
            contact_schema.load(request_data)
            contact.update(request_data)
            db.session.commit()
            flash("Contact updated.", "success")
        except ValidationError as err:
            errors = err.normalized_messages()
            flash("There is one form error.", "error")

    data = {
        "errors": errors,
        "contact": contact_schema.dump(contact),
        "organizations": organizations,
    }
    return render_inertia("contacts/Edit", props=data)


@contact_routes.route("/<contact_id>/delete/", methods=["DELETE"])
@login_required
def delete(contact_id: int):
    contact = Contact.query.get_or_404(contact_id)
    contact.deleted_at = datetime.now()
    db.session.commit()
    flash("Contact deleted.", "success")
    return redirect(url_for("contacts.edit", contact_id=contact_id))


@contact_routes.route("/<contact_id>/restore/", methods=["PUT"])
@login_required
def restore(contact_id: int):
    contact = Contact.query.get_or_404(contact_id)
    contact.deleted_at = None
    db.session.commit()
    flash("Contact restored.", "success")
    return redirect(url_for("contacts.edit", contact_id=contact_id))
