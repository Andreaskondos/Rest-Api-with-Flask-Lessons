from db import db


class TagItems(db.Model):
    __tablename__ = "tag_items"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(
        db.Integer, db.ForeignKey("items.id"), unique=False, nullable=False
    )
    tag_id = db.Column(
        db.Integer, db.ForeignKey("tags.id"), unique=False, nullable=False
    )
