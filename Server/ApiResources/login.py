from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from Server.utils import *
from Server.data import *
from Server.user import *

class Login(Resource):

    def get(self):
        """
        Posting login data in order to get the token.
        """
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("hash")
        params = parser.parse_args()
        if "username" not in params.keys() or "hash" not in params.keys():
            return {"error": "Missing informations"}, 400


        if value_in_database("username", params["username"]):
            user = User(cnx, params["username"])
            if user.hash != params["hash"]:
                return {"error": "Invalid credidentials"}, 403
            return {"token": user.token}, 200
        else:
            return {"error": "Invalid credidentials"}, 403

    def put(self):
        """
        Register in the database
        """

        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("hash")
        parser.add_argument("invited_by")
        params = parser.parse_args()

        if not params["username"] or not params["hash"] or (not params["invited_by"] and params["username"] != DEFAULT_FIRST_USERNAME):
            return {"error": "Missing informations"}, 400

        if not value_in_database("invite_code", params["invited_by"]) and params["username"] != DEFAULT_FIRST_USERNAME:
            return {"error": "This invitation code is not valid"}, 403

        if value_in_database("username", params["username"]):
            return {"error": "Username is already taken"}, 403


        token = generate_token()
        while value_in_database("token", token):
            token = generate_token()
        invite_code = generate_invite_code()
        while value_in_database("invite_code", invite_code):
            invite_code = generate_invite_code()

        cursor = cnx.cursor()
        query = f"""INSERT INTO UserData VALUES ('{params['username']}', '{params['hash']}', '{token}', '{invite_code}', '{'nonea' if params['username'] == DEFAULT_FIRST_USERNAME else params['invited_by']}', {ORIGINAL_MONEY_INVESTMENT});"""
        print(query)
        cursor.execute(query)
        cursor.close()
        user = User(cnx, params["username"])
        if params["username"] != DEFAULT_FIRST_USERNAME : share_money_from(user)

        return {"token": token}


