from flask import Blueprint, render_template, request, redirect, send_file
from flask_login import login_required, current_user
from . import db
from .models import File
import io

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template("login.html")

@main.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        file = request.files["file"]
        new_file = File(
            filename=file.filename,
            data=file.read(),
            mimetype=file.mimetype,
            owner=current_user
        )
        db.session.add(new_file)
        db.session.commit()
    files = File.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", files=files)

@main.route("/download/<int:file_id>")
@login_required
def download(file_id):
    file = File.query.get_or_404(file_id)
    return send_file(io.BytesIO(file.data), download_name=file.filename, mimetype=file.mimetype)
