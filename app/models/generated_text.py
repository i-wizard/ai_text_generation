from app import db
from datetime import datetime, timezone


def current_datetime() -> datetime:
    return datetime.now(timezone.utc)


class GeneratedText(db.Model):
    __tablename__ = "generated_texts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=current_datetime)

    user = db.relationship("User", backref=db.backref("generated_texts", lazy=True))
