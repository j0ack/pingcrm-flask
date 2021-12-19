"""Ping CRM cli to add fake data."""

from random import choice

import click
from flask.cli import with_appcontext

from app import db
from app.factories import (
    AccountFactory,
    ContactFactory,
    OrganizationFactory,
    UserFactory,
)


@click.command("seed")
@with_appcontext
def seed():
    account = AccountFactory(name="Acme Corporation")
    db.session.add(account)

    user = UserFactory(
        first_name="John",
        last_name="Doe",
        email="johndoe@example.com",
        account=account,
        owner=True,
    )
    user.set_password("secret")
    db.session.add(user)

    for _ in range(5):
        user = UserFactory(account=account)
        db.session.add(user)

    organizations = []
    for _ in range(100):
        organization = OrganizationFactory(account=account)
        db.session.add(organization)
        organizations.append(organization)

    for _ in range(100):
        contact = ContactFactory(account=account, organization=choice(organizations))
        db.session.add(contact)

    db.session.commit()
