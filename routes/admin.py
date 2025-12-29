from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.admin import Admin
from models.listing import Listing
from extensions import db
from functools import wraps

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "admin_id" not in session:
            flash("Admin login required", "warning")
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return wrapper


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]

        admin = Admin.query.filter_by(username=user).first()

        if admin and admin.check_password(pw):
            session["admin_id"] = admin.id
            return redirect(url_for("admin.dashboard"))
        flash("Invalid credentials", "danger")

    return render_template("listings/adminlogin.html")


@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    # support search + pagination for admin dashboard
    q = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 6

    query = Listing.query
    if q:
        query = query.filter(
            Listing.title.ilike(f"%{q}%") |
            Listing.description.ilike(f"%{q}%")
        )

    pagination = query.paginate(page=page, per_page=per_page)
    listings = pagination.items

    return render_template(
        "listings/index.html",
        listings=listings,
        pagination=pagination,
        is_admin=True,
        q=q
    )


@admin_bp.route("/logout")
@admin_required
def logout():
    session.pop("admin_id")
    return redirect(url_for("admin.login"))