from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship("ItemModel", lazy="dynamic", back_populates="store", cascade="all, delete")
    tags = db.relationship("TagModel", lazy="dynamic", back_populates="store")
    
    def __init__(self, name):
        self.name = name
    
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "items": [item.json() for item in self.items.all()]
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