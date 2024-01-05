from flask.views import MethodView
from flask_smorest import abort, Blueprint
from models import ItemModel
from schemas import ItemListSchema, ItemSchema, ItemUpdateSchema
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        return ItemModel.find_by_id(item_id)

    def delete(self, item_id):
        item = ItemModel.find_by_id(item_id)
        try:
            item.delete_from_db()
            return {"message": "item deleted"}
        except KeyError:
            abort(404, message="item not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.find_by_id(item_id)
        item.price = item_data["price"]
        item.name = item_data["name"]
        try:
            item.save_to_db()
        except SQLAlchemyError:
            abort(500, message="item could not be saved")
        return item

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemListSchema)
    def get(self):
        return {"items": ItemModel.find_all()}

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="user not authorized")
        item = ItemModel(**item_data)

        try:
            item.save_to_db()
        except SQLAlchemyError as e:
            abort(500, message="item could not be saved")
        return item