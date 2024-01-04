from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import TagModel
from sqlalchemy.exc import SQLAlchemyError
from models import ItemModel
from models import ItemTags

from schemas import TagAndItemSchema, TagListSchema, TagSchema


blp = Blueprint("tags", __name__, description="Operations on tags")

@blp.route("/store/<int:store_id>/tag")
class TagList(MethodView):
    @blp.response(200, TagListSchema)
    def get(self, store_id):
        return {"tags": TagModel.find_all(store_id)}
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            tag = tag.save_to_db()
        except SQLAlchemyError:
            abort(500, message="tag could not be saved")
        return tag    

@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.find_by_id(tag_id)
        return tag
    
    @blp.response(202, description="delete a tag if no item associated with it", 
                  example="{message: 'tag deleted'}")
    @blp.alt_response(404, description="tag not found", example="{message: 'tag not found'}")
    @blp.alt_response(400, description="tag still associated with items", 
                      example="{message: 'tag still associated with items'}")
    def delete(self, tag_id):
        tag = TagModel.find_by_id(tag_id)
        if not tag.items:    
            try:
                tag.delete_from_db()
                return {"message": "tag deleted"}
            except SQLAlchemyError:
                abort(500, message="tag could not be deleted")
        abort(400, message="tag still associated with items")
    
    @blp.arguments(TagSchema)
    @blp.response(200, TagSchema)
    def put(self, tag_data, tag_id):
        tag = TagModel.find_by_id(tag_id)
        tag.name = tag_data["name"]
        try:
            tag.save_to_db()
        except SQLAlchemyError:
            abort(500, message="tag could not be saved")
        return tag

@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        tag = TagModel.find_by_id(tag_id)
        item = ItemModel.find_by_id(item_id)
        item.tags.append(tag)
        try:
            item.save_to_db()
        except SQLAlchemyError:
            abort(500, message="tag could not be saved")
        return tag
    
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.find_by_id(item_id)
        tag = TagModel.find_by_id(tag_id)
        item.tags.remove(tag)
        try:
            item.save_to_db()
            return {"message": "tag deleted", "item":item, "tag":tag}
        except SQLAlchemyError:
            abort(500, message="tag could not be deleted")