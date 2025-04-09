from flask import Blueprint, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import login_user, logout_user
from .models import User
from . import db, login_manager

auth_bp = Blueprint('auth', __name__)

google_bp = make_google_blueprint(
    scope=["profile", "email"],
    redirect_url="/login/google/authorized"
)
auth_bp.register_blueprint(google_bp, url_prefix="/login")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route("/login/google/authorized")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    email = resp.json()["email"]
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for("main.dashboard"))

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
