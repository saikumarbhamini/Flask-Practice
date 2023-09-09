from sqlalchemy.sql import func

from utilities.database import db
from utilities.security import generate_token


class Token(db.Model):
    token = db.Column(db.String(20), default=generate_token, primary=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created = db.Column(db.DateTime, default=func.now())
