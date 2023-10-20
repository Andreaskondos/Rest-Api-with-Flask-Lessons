from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel, StoreModel, TagModel
from schemas import TagSchema

blp = Blueprint("Tags", __name__, description="Operations for tags")


@blp.route("/store/<int:store_id>/tag")
class TagInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(404, message=str(e))
        return tag


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        return TagModel.query.get_or_404(tag_id)

    @blp.response(202, description="Deleting a tag", example={"message": "Tag deleted"})
    @blp.alt_response(404, description="Tag not found")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case tag is not deleted",
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted"}
        abort(400, "Tag is assigned to one or more items and can not be deleted")


@blp.route("/tag")
class TagList(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self):
        return TagModel.query.all()


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "An error occured while inserting the tag")
        return tag

    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "An error occured while deleting the tag")
        return {
            "message": "You have successfully removed the tag",
            "item": item,
            "tag": tag,
        }
