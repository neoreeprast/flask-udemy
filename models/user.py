from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(), unique=False, nullable=False)
    refresh_token = db.Column(db.String(), unique=False, nullable=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

