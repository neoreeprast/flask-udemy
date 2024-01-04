from db import db

class ItemTags(db.Model):
    __tablename__ = "item_tags"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), unique=False, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), unique=False, nullable=False)

    __table_args__ = (
        db.ForeignKeyConstraint([item_id], ["items.id"], ondelete="CASCADE"),
        db.ForeignKeyConstraint([tag_id], ["tags.id"], ondelete="CASCADE"),
    )

    @classmethod
    def find_all(cls, item_id):
        return cls.query.filter_by(item_id=item_id).all()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self