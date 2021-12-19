"""Ping CRM account model."""

from app import db
from app.models import BaseModel


class Account(BaseModel):

    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
