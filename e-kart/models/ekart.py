import enum

from sqlalchemy.sql import func

from models.user import User
from utilities.database import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255), unique=True, nullable=False)


class Sizes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(5), nullable=False)


class Ekart(db.Model):
    """Ekart Model"""

    class Gender(enum.Enum):
        MALE = "M"
        FEMALE = "F"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(
        db.Integer, db.ForeignKey("category.id", ondelete="CASCADE"), nullable=False
    )
    gender = db.Column(db.Enum(Gender))
    product_code = db.Column(db.String(255), unique=True, nullable=False)
    product_name = db.Column(db.String(255))
    available_quantity = db.Column(db.Integer)
    size_id = db.Column(
        db.Integer, db.ForeignKey("sizes.id", ondelete="CASCADE"), nullable=False
    )
    price = db.Column(db.Float)
    created = db.Column(db.DateTime, default=func.now())
    updated = db.Column(
        db.DateTime, default=func.now(), onupdate=func.current_timestamp()
    )


class CartItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_item = db.Column(
        db.Integer, db.ForeignKey("ekart.id", ondelete="CASCADE"), nullable=False
    )
    quantity = db.Column(db.Integer)
    added_datetime = db.Column(db.DateTime, default=func.now())
    updated = db.Column(
        db.DateTime, default=func.now(), onupdate=func.current_timestamp()
    )
    total_price = db.Column(db.Float)
    user = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))


class WishList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_item = db.Column(
        db.Integer,
        db.ForeignKey("ekart.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    added_datetime = db.Column(db.DateTime, default=func.now())
    user = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
