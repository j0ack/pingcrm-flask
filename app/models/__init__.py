"""Ping CRM base models."""

from typing import Any, Dict

from app import db


class BaseModel(db.Model):

    __abstract__ = True

    deleted_at = db.Column(db.DateTime, nullable=True)

    def update(self, data: Dict[str, Any]):
        for key, value in data.items():
            setattr(self, key, value)
