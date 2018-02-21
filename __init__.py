from flask import Flask, request
from flask_restful import Resource, Api

import database as db

app = Flask(__name__)
api = Api(app)


class Bands(Resource):
    def get(self):
        return list(db.get_all_nodes('band'))


class Band(Resource):
    def get(self, username):
        return db.get_node('band', 'username', username)


class Band_Events(Resource):
    def get(self, username):
        return db.get_related_nodes('band', 'username', username, 'event')


class Cities(Resource):
    def get(self):
        return list(db.get_all_nodes('city'))


class City(Resource):
    def get(self, name):
        return db.get_node('city', 'name', name)


class City_Venues(Resource):
    def get(self, name):
        return db.get_related_nodes('city', 'name', name, 'venue')


api.add_resource(Bands, '/bands')
api.add_resource(Band, '/bands/<username>')
api.add_resource(Band_Events, '/bands/<username>/events')
api.add_resource(Cities, '/cities')
api.add_resource(City, '/cities/<name>')
api.add_resource(City_Venues, '/cities/<name>/venues')
# api.add_resource(Venues, '/venues')
# api.add_resource(Events, '/events')


if __name__ == '__main__':
    app.run(port=5002)
