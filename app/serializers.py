"""PingCRM serializers."""

from typing import Any, Dict

from marshmallow import fields, post_load, validate

from app import ma
from app.models.contact import Contact
from app.models.organization import Organization
from app.models.user import User


class ContactSchema(ma.Schema):
    """Contact serialization class."""

    class Meta:
        fields = (
            "id",
            "name",
            "organization_id",
            "organization",
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "city",
            "region",
            "country",
            "postal_code",
            "deleted_at",
        )

    first_name = fields.String(
        required=True,
        validate=validate.Length(
            min=1,
            error="This field is required",
        ),
    )
    last_name = fields.String(
        required=True,
        validate=validate.Length(
            min=1,
            error="This field is required",
        ),
    )
    organization = ma.Nested("OrganizationSchema", exlude=["contacts"])

    @post_load(pass_many=False)
    def make_contact(self, data: Dict[str, Any], **kwargs) -> Contact:
        contact = Contact(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
            city=data.get("city"),
            region=data.get("region"),
            country=data.get("country"),
            postal_code=data.get("postal_code"),
            organization_id=data.get("organization_id"),
        )

        return contact


class OrganizationSchema(ma.Schema):
    """Organization serializer class."""

    class Meta:
        fields = (
            "id",
            "name",
            "email",
            "phone",
            "address",
            "city",
            "region",
            "country",
            "postal_code",
            "contacts",
            "deleted_at",
        )

    name = fields.String(
        required=True,
        validate=validate.Length(
            min=1,
            error="This field is required",
        ),
    )
    contacts = ma.Nested("ContactSchema", many=True, exclude=["organization"])

    @post_load(pass_many=False)
    def make_organization(self, data: Dict[str, Any], **kwargs) -> Organization:
        organization = Organization(
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            city=data.get("city"),
            address=data.get("address"),
            region=data.get("region"),
            country=data.get("country"),
            postal_code=data.get("postal_code"),
        )

        return organization


class UserSchema(ma.Schema):
    """User serializer class."""

    class Meta:
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "photo_path",
            "owner",
            "deleted_at",
        )

    first_name = fields.String(
        required=True,
        validate=validate.Length(
            min=1,
            error="This field is required",
        ),
    )
    last_name = fields.String(
        required=True,
        validate=validate.Length(
            min=1,
            error="This field is required",
        ),
    )
    email = fields.Email(
        required=True,
        validate=validate.Length(
            min=1,
            error="This field is required",
        ),
    )
    password = fields.String(
        required=True,
        validate=validate.Length(
            min=1,
            error="This field is required",
        ),
    )

    @post_load(pass_many=False)
    def make_user(self, data, **kwargs):
        user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            owner=data.get("owner") == 1,
        )
        if pwd := data.get("password"):
            user.set_password(pwd)

        return user


contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)
organization_schema = OrganizationSchema()
organizations_schema = OrganizationSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
