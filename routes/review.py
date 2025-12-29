from flask import Blueprint, request, redirect, url_for, flash
from extensions import db
from models.review import Review

review_bp = Blueprint("review", __name__, url_prefix="/reviews")


@review_bp.route("/add/<int:listing_id>", methods=["POST"])
def add_review(listing_id):
    r = Review(
        username=request.form["username"],
        rating=request.form["rating"],
        comment=request.form["comment"],
        listing_id=listing_id
    )

    db.session.add(r)
    db.session.commit()

    flash("Review submitted successfully!", "success")
    return redirect(url_for("listing.show", id=listing_id))
