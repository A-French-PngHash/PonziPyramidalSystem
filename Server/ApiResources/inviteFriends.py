from Server.utils import *
from flask_restful import Resource, Api, request
from Server.user import *

class InviteFriends(Resource):
    def get(self):
        """Return the authentication code"""
        token = request.headers.get('Authentication')
        if not value_in_database("token", token) or token == None:
            return {"error" : "Authentication failed. Token is invalid."}, 403

        user = User(cnx, None, token)

        return {"invite_code" : user.invite_code}

