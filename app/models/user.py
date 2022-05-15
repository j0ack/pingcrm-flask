"""Ping CRM user model."""


from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import BaseModel
from app.models.account import Account


class User(UserMixin, BaseModel):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    photo_path = db.Column(db.String)
    owner = db.Column(db.Boolean, nullable=False, default=False)

    account_id = db.Column(db.Integer, db.ForeignKey(Account.id), nullable=False)
    account = db.relationship(Account, backref=db.backref("users"))

    def set_password(self, value: str):
        self.password = generate_password_hash(value)

    def check_password(self, pwd: str) -> bool:
        return check_password_hash(self.password, pwd)
