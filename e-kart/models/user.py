from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash

from utilities.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    date_of_join = db.Column(db.DateTime, default=func.now())
    last_login = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        stored_hash = check_password_hash(self.password, password)
        generated_hash = generate_password_hash(password)
        current_hash = check_password_hash(generated_hash, password)
        return stored_hash == current_hash

    def __repr__(self):
        return f"{self.__class__.__name__}"
