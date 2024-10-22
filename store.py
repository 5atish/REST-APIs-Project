import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores


blp = Blueprint("stores", __name__, description="Operation on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    """docstring for Store."""

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

    # def __init__(self, arg):
    #     super(Store, self).__init__()
    #     self.arg = arg
