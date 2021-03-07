from flask import Flask, request
from flask_restful import Resource, Api
from ApiResources.inviteFriends import *
from ApiResources.login import *
from utils import *
from data import *
from ApiResources.money import *

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
