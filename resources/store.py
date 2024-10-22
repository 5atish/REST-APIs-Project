import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items
from schemas import StoreSchemas


blp = Blueprint("stores", __name__, description="Operation on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchemas)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            return abort(404,message="store not found.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            return abort(404,message="Store not found.")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchemas(many=True))
    def get(self):
        # return {"stores": list(stores.values())}
        return stores.values()

    @blp.arguments(StoreSchemas)
    @blp.response(200, StoreSchemas)
    def post(self, store_data):
        # store_data = request.get_json()
        # if "name" not in store_data:
        #     abort(400, message="Bad request. Ensure 'name' is included in the JSON playload'")

        for store in stores.values():
            if stores_data["name"] == store["name"]:
                abort(400, message="Store already exist.")
        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id }
        stores[store_id] = store
        return store, 201
