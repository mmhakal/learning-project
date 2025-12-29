from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from extensions import db
from models.super_admin import SuperAdmin
from models.admin import Admin
from models.user import User

super_admin_bp = Blueprint("super_admin", __name__, url_prefix="/super-admin")


# ─────────────────────────────
# 🔐 Super Admin Required
# ─────────────────────────────
def super_admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "super_admin_id" not in session:
            flash("Super Admin login required", "warning")
            return redirect(url_for("super_admin.login"))
        return f(*args, **kwargs)
    return wrapper


# ─────────────────────────────
# 🔐 Super Admin Login
# ─────────────────────────────
@super_admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sa = SuperAdmin.query.filter_by(username=username).first()
        if sa and sa.check_password(password):
            session["super_admin_id"] = sa.id
            flash("Welcome Super Admin!", "success")
            return redirect(url_for("super_admin.dashboard"))

        flash("Invalid Super Admin credentials", "danger")

    return render_template("super_admin/login.html")


# ─────────────────────────────
# 🛡️ Super Admin Dashboard
# ─────────────────────────────
@super_admin_bp.route("/dashboard")
@super_admin_required
def dashboard():
    admins = Admin.query.all()
    users = User.query.all()

    return render_template(
        "super_admin/dashboard.html",
        admins=admins,
        users=users
    )


# ─────────────────────────────
# ➕ Add Admin
# ─────────────────────────────
@super_admin_bp.route("/add-admin", methods=["POST"])
@super_admin_required
def add_admin():
    username = request.form["username"]
    password = request.form["password"]

    if Admin.query.filter_by(username=username).first():
        flash("Admin already exists", "danger")
        return redirect(url_for("super_admin.dashboard"))

    admin = Admin(username=username)
    admin.set_password(password)

    db.session.add(admin)
    db.session.commit()

    flash("Admin created successfully", "success")
    return redirect(url_for("super_admin.dashboard"))


# ─────────────────────────────
# ❌ Delete Admin
# ─────────────────────────────
@super_admin_bp.route("/delete-admin/<int:id>", methods=["POST"])
@super_admin_required
def delete_admin(id):
    admin = Admin.query.get_or_404(id)

    db.session.delete(admin)
    db.session.commit()

    flash("Admin deleted successfully", "info")
    return redirect(url_for("super_admin.dashboard"))


# ─────────────────────────────
# ❌ Delete User
# ─────────────────────────────
@super_admin_bp.route("/delete-user/<int:id>", methods=["POST"])
@super_admin_required
def delete_user(id):
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully", "info")
    return redirect(url_for("super_admin.dashboard"))


# ─────────────────────────────
# 🚪 Logout Super Admin
# ─────────────────────────────
@super_admin_bp.route("/logout")
@super_admin_required
def logout():
    session.pop("super_admin_id", None)
    flash("Logged out successfully", "info")
    return redirect(url_for("super_admin.login"))
