from flask import Flask, render_template
from flask_migrate import Migrate
from extensions import db, login_manager

migrate = Migrate()


def create_app():
    app = Flask(
        __name__,
        static_folder="public",
        template_folder="views"
    )

    # ─────────────────────────────
    # CONFIG
    # ─────────────────────────────
    app.config["SECRET_KEY"] = "mysecretkey"

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://root:1234@127.0.0.1:3306/flask_app"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ─────────────────────────────
    # EXTENSIONS
    # ─────────────────────────────
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "user.login"
    login_manager.login_message_category = "warning"

    # ─────────────────────────────
    # MODELS (IMPORT ONCE)
    # ─────────────────────────────
    from models.user import User
    from models.admin import Admin
    from models.super_admin import SuperAdmin
    from models.listing import Listing
    from models.review import Review

    # ─────────────────────────────
    # CREATE DATABASE TABLES
    # ─────────────────────────────
    with app.app_context():
        db.create_all()

        # Create default Admin
        if not Admin.query.first():
            admin = Admin(username="admin")
            admin.set_password("admin123")
            db.session.add(admin)

        # Create default Super Admin
        if not SuperAdmin.query.first():
            sa = SuperAdmin(username="superadmin")
            sa.set_password("super123")
            db.session.add(sa)

        db.session.commit()

    # ─────────────────────────────
    # BLUEPRINTS
    # ─────────────────────────────
    from routes.user import user_bp
    from routes.admin import admin_bp
    from routes.super_admin import super_admin_bp
    from routes.listing import listing_bp
    from routes.review import review_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(super_admin_bp)
    app.register_blueprint(listing_bp)
    app.register_blueprint(review_bp)

    # ─────────────────────────────
    # HOME PAGE
    # ─────────────────────────────
    @app.route("/")
    def home():
        listings = Listing.query.order_by(Listing.id.desc()).limit(6).all()
        return render_template("home.html", listings=listings)

    # ─────────────────────────────
    # ERROR HANDLER
    # ─────────────────────────────
    from utils.Error import AppError

    @app.errorhandler(AppError)
    def error(e):
        return render_template(
            "error.html",
            message=e.message,
            status_code=e.status_code
        ), e.status_code

    return app


# ─────────────────────────────
# RUN APP
# ─────────────────────────────
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
