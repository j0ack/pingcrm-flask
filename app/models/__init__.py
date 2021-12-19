"""Ping CRM base models."""

from app import db


class BaseModel(db.Model):

    __abstract__ = True

    deleted_at = db.Column(db.DateTime, nullable=True)
