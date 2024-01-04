from db import db

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)

    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", secondary="item_tags", back_populates="tags")

    __table_args__ = (
        db.ForeignKeyConstraint([store_id], ["stores.id"], ondelete="CASCADE"),
    )

    @classmethod
    def find_all(cls, store_id):
        return cls.query.filter_by(store_id=store_id).all()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self