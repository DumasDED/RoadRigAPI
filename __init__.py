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


api.add_resource(Bands, '/bands')
api.add_resource(Band, '/bands/<username>')
api.add_resource(Band_Events, '/bands/<username>/events')
# api.add_resource(Venues, '/venues')
# api.add_resource(Events, '/events')


if __name__ == '__main__':
    app.run(port=5002)
