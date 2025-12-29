from extensions import db


class Listing(db.Model):
    __tablename__ = "listings"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    price = db.Column(db.Integer)

    reviews = db.relationship("Review", backref="listing", cascade="all, delete")
