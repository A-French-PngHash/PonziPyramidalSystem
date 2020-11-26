from flask import Flask, request
from flask_restful import Resource, Api
from Server.ApiResources.inviteFriends import *
from Server.ApiResources.login import *
from Server.utils import *
from Server.data import *
from Server.ApiResources.money import *
import Server.mysqlconnection

"""
username : Organisator
hash : fSizAEtY9SvjrvJbKiWcKGwvHOAmdFiJX6bEO6tPv3g
"""

app = Flask(__name__)
api = Api(app)

api.add_resource(Login, '/login')
api.add_resource(InviteFriends, '/invite')
api.add_resource(Money, '/money')

app.run(port=PORT)
