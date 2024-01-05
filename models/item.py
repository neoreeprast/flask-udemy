from db import db

class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    description = db.Column(db.String)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id", ondelete="CASCADE", name="item_stores_fk"), unique=False, nullable=False)
    store = db.relationship("StoreModel", back_populates="items")
    tags = db.relationship("TagModel", back_populates="items", secondary="item_tags")
    
    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
    
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "store_id": self.store_id
        }
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()