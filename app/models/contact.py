"""Ping CRM contact model."""

from typing import Any, Dict

from app import db
from app.models import BaseModel
from app.models.account import Account
from app.models.organization import Organization


class Contact(BaseModel):

    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    region = db.Column(db.String)
    country = db.Column(db.String)
    postal_code = db.Column(db.String)

    account_id = db.Column(db.Integer, db.ForeignKey(Account.id), nullable=False)
    account = db.relationship(Account, backref=db.backref("contacts"))

    organization_id = db.Column(
        db.Integer, db.ForeignKey(Organization.id), nullable=False
    )
    organization = db.relationship(Organization, backref=db.backref("contacts"))

    @property
    def name(self) -> str:
        return f"{self.last_name} {self.first_name}"

    def to_dict(self) -> Dict[str, Any]:
        """JSON representation."""
        return {
            "id": self.id,
            "name": self.name,
            "organization_id": self.organization.id,
            "organization": {"name": self.organization.name},
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "city": self.city,
            "region": self.region,
            "country": self.country,
            "postal_code": self.postal_code,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else "",
        }
