import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from schemas import ItemSchema, ItemUpdateSchemas


blp = Blueprint("Items",__name__, description="Operation on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404,message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404,message="Item not found.")

    @blp.arguments(ItemUpdateSchemas)
    @blp.response(200, ItemSchema)
    def put(self,item_data, item_id):

        # item_data = request.get_json()
        # if ("price" not in item_data or "store_id" not in item_data or "name" not in item_data):
        #     abort(400, message="Bad request. Ensure 'price', 'store_id', and 'name' are included in JSON payload.")

        try:
            item = items[item_id]
            item |= item_data
            return item
        except:
            abort(404, message="Item not found.")

        if ("price" not in item_data or "store_id" not in item_data or "name" not in item_data):
            abort(400, message="Bad request. Ensure 'price', 'store_id', and 'name' are included in JSON payload.")
        for item in items.values():
            if ( item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]):
                abort(404, message="Item already exist.")
        if item_data["store_id"] not in stores:
            return abort(404,message="store not found.")
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id }
        items[item_id] = item
        return item, 201

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        # return {"items": list(items.values())}
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # item_data = request.get_json()
        # if ("price" not in item_data or "store_id" not in item_data or "name" not in item_data):
        #     abort(400, message="Bad request. Ensure 'name', 'price', 'store_id' is included in the JSON playload'")

        for item in items.values():
            if (item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]):
                abort(400, message="Item already exist.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id }
        items[item_id] = item
        return item, 201
