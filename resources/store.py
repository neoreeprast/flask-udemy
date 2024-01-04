import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from models import StoreModel
from schemas import StoreListSchema, StoreSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        return StoreModel.find_by_id(store_id)
    

    def delete(self, store_id):
        store = StoreModel.find_by_id(store_id)
        try:
            store.delete_from_db()    
            return {"message": "store deleted"}
        except IntegrityError:
            abort(400, message="cannot delete store with items")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreListSchema)
    def get(self):
        
        return {"stores": StoreModel.find_all()}

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        new_store = StoreModel(**store_data)
        try:
            new_store = new_store.save_to_db()
        except IntegrityError:
            abort(400, message="store already exists")
        except SQLAlchemyError:
            abort(500, message="store could not be saved")
        return new_store