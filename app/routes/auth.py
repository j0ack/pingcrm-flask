"""Ping CRM auth routes."""

from flask import Blueprint, flash, redirect, request, url_for
from flask_inertia import render_inertia
from flask_login import login_required, login_user, logout_user

from app import login_manager
from app.models.user import User

auth = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(user_id)


@auth.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        request_data = request.get_json()
        email = request_data.get("email")
        password = request_data.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password", "error")
    return render_inertia("Login")


@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
