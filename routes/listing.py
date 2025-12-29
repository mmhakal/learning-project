from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import db
from models.listing import Listing
from models.review import Review
from routes.admin import admin_required

# Blueprint for listings
listing_bp = Blueprint("listing", __name__, url_prefix="/listings")


# ─────────────────────────────
# List all listings + SEARCH + PAGINATION
# ─────────────────────────────
@listing_bp.route("/")
def index():
    q = request.args.get("q", "").strip()              # search query
    page = request.args.get("page", 1, type=int)       # current page
    per_page = 6                                       # items per page

    query = Listing.query

    # Apply search filter if q exists
    if q:
        query = query.filter(
            Listing.title.ilike(f"%{q}%") |
            Listing.description.ilike(f"%{q}%")
        )

    # Pagination
    pagination = query.paginate(page=page, per_page=per_page)
    listings = pagination.items

    is_admin = "admin_id" in session

    return render_template(
        "listings/index.html",
        listings=listings,
        pagination=pagination,
        is_admin=is_admin,
        q=q
    )


# ─────────────────────────────
# Create a new listing
# ─────────────────────────────
@listing_bp.route("/new", methods=["GET", "POST"])
@admin_required
def new():
    if request.method == "POST":
        listing = Listing(
            title=request.form["title"],
            description=request.form["description"],
            image_url=request.form["image_url"],
            price=request.form["price"],
        )
        db.session.add(listing)
        db.session.commit()
        flash("Listing created successfully!", "success")
        return redirect(url_for("listing.index"))

    return render_template("listings/new.html")


# ─────────────────────────────
# Show listing details
# ─────────────────────────────
@listing_bp.route("/<int:id>")
def show(id):
    listing = Listing.query.get_or_404(id)
    reviews = Review.query.filter_by(listing_id=id).all()
    is_admin = "admin_id" in session

    return render_template(
        "listings/show.html",
        listing=listing,
        reviews=reviews,
        is_admin=is_admin,
    )


# ─────────────────────────────
# Edit listing
# ─────────────────────────────
@listing_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@admin_required
def edit(id):
    listing = Listing.query.get_or_404(id)

    if request.method == "POST":
        listing.title = request.form["title"]
        listing.description = request.form["description"]
        listing.image_url = request.form["image_url"]
        listing.price = request.form["price"]

        db.session.commit()
        flash("Listing updated!", "success")
        return redirect(url_for("listing.show", id=id))

    return render_template("listings/edit.html", listing=listing)


# ─────────────────────────────
# Delete listing
# ─────────────────────────────
@listing_bp.route("/<int:id>/delete", methods=["POST"])
@admin_required
def delete(id):
    listing = Listing.query.get_or_404(id)
    db.session.delete(listing)
    db.session.commit()
    flash("Listing deleted!", "info")
    return redirect(url_for("listing.index"))
