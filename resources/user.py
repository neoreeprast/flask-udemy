import bcrypt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import UserModel

from schemas import LoginSchema, UserSchema
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token, get_jti, get_jwt, get_jwt_identity, jwt_required


blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/user")
class User(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        username = user_data["username"]
        password = user_data["password"]
        user = UserModel.find_by_username(username)
        if user:
            abort(400, message="user already exists")

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user = UserModel(username=username, password_hash=password_hash)
        try:
            user = user.save_to_db()
        except SQLAlchemyError:
            abort(500, message="user could not be saved")
        return user
    
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200, LoginSchema)
    def post(self, user_data):
        username = user_data["username"].lower()
        password = user_data["password"]
        user = UserModel.find_by_username(username)
        if user and bcrypt.checkpw(password.encode("utf-8"), user.password_hash):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            decoded_token = decode_token(refresh_token)
            user.refresh_token = decoded_token["jti"]
            user.save_to_db()
            return {"access_token": access_token, 
                    "refresh_token": refresh_token}    
        abort(401, message="user or password invalid")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if user and user.refresh_token == get_jwt()["jti"]:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            decoded_token = decode_token(refresh_token)
            user.refresh_token = decoded_token["jti"]
            user.save_to_db()
            return {"access_token": access_token, "refresh_token": refresh_token}    
        abort(401, message="invalid refresh token")