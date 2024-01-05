from db import db

class ItemTags(db.Model):
    __tablename__ = "item_tags"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id", ondelete="CASCADE", name="item_tags_items_fk"), unique=False, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id",ondelete="CASCADE", name="item_tags_tags_fk"), unique=False, nullable=False)

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