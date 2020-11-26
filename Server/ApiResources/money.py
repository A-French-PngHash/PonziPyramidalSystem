from flask import request
from flask_restful import Resource, Api, reqparse
from Server.utils import *
from Server.data import *


class Money(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("amount")
        params = parser.parse_args()
        token = request.headers.get('Authentication')

        try:
            user = User(cnx, token=token)
        except:
            return {"error": "Invalid credidentials"}, 403

        if not params["amount"]:
            # In this case the user just want to know his balance
            return {"balance" : user.money}, 200

        else:
            try:
                amount = int(params["amount"])
            except:
                return {"error" : "The \"amount\" parameter must be a number"}, 400

            amount = amount if user.money >= amount else user.money
            user.money -= amount
            return {"amount" : amount}


