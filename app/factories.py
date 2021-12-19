"""Ping CRM fake data factories."""

from random import randint

from factory import Faker, LazyFunction, SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from app import db
from app.models.account import Account
from app.models.contact import Contact
from app.models.organization import Organization
from app.models.user import User


def postal_code() -> str:
    dept_code = str(randint(1, 98)).zfill(2)
    city_code = str(randint(1, 99)).ljust(3, "0")
    return f"{dept_code}{city_code}"


class AccountFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Account
        sqlalchemy_session = db.session

    name = Faker("name")


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    first_name = Faker("first_name", locale="fr_FR")
    last_name = Faker("last_name", locale="fr_FR")
    email = Faker("email", locale="fr_FR")
    password = Faker("password")
    account = SubFactory(AccountFactory)


class OrganizationFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Organization
        sqlalchemy_session = db.session

    name = Faker("company", locale="fr_FR")
    email = Faker("email", locale="fr_FR")
    phone = Faker("phone_number", locale="fr_FR")
    address = Faker("street_address", locale="fr_FR")
    city = Faker("city", locale="fr_FR")
    region = Faker("region", locale="fr_FR")
    country = "France"
    postal_code = LazyFunction(postal_code)
    account = SubFactory(AccountFactory)


class ContactFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Contact
        sqlalchemy_session = db.session

    first_name = Faker("first_name", locale="fr_FR")
    last_name = Faker("last_name", locale="fr_FR")
    email = Faker("email", locale="fr_FR")
    phone = Faker("phone_number", locale="fr_FR")
    address = Faker("street_address", locale="fr_FR")
    city = Faker("city", locale="fr_FR")
    region = Faker("region", locale="fr_FR")
    country = "France"
    postal_code = LazyFunction(postal_code)
    account = SubFactory(AccountFactory)
    organization = SubFactory(OrganizationFactory)
