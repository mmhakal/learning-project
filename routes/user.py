from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from extensions import db
from flask_login import login_user, logout_user, login_required

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # -------------------------
        # CHECK for duplicate user
        # -------------------------
        if User.query.filter_by(username=username).first():
            flash("Username already exists. Choose another one.", "danger")
            return redirect(url_for("user.signup"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please login.", "danger")
            return redirect(url_for("user.signup"))

        # Create user
        u = User(username=username, email=email)
        u.set_password(password)

        db.session.add(u)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for("user.login"))

    return render_template("users/signup.html")


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        pw = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(pw):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("listing.index"))

        flash("Invalid email or password", "danger")

    return render_template("users/login.html")


@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("user.login"))
