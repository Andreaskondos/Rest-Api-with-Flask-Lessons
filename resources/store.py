from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("Stores", __name__, description="Operations for stores")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return StoreModel.query.get_or_404(store_id)
        except KeyError:
            abort(404, message="Store not found")

    def put(self, store_id):
        raise NotImplementedError("Update store is not yet implemented")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        new_store = StoreModel(**store_data)

        try:
            db.session.add(new_store)
            db.session.commit()
        except IntegrityError:
            abort(400, "This store's name already exists")
        except SQLAlchemyError:
            abort(500, "An error occured while crating the store")
        return new_store
