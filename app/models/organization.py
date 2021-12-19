"""Ping CRM organization model."""

from app import db
from app.models import BaseModel
from app.models.account import Account


class Organization(BaseModel):

    __tablename__ = "organizations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    region = db.Column(db.String)
    country = db.Column(db.String)
    postal_code = db.Column(db.String)

    account_id = db.Column(db.Integer, db.ForeignKey(Account.id), nullable=False)
    account = db.relationship(Account, backref=db.backref("organizations"))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "city": self.city,
            "region": self.region,
            "country": self.country,
            "postal_code": self.postal_code,
            "contacts": [contact.to_dict() for contact in self.contacts],
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else "",
        }
