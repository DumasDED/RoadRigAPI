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


class BandEvents(Resource):
    def get(self, username):
        return db.get_child_nodes('band', 'username', username, 'event')


class CityStateList(Resource):
    def get(self):
        return db.get_related_nodes('city', 'state')


class Cities(Resource):
    def get(self):
        return list(db.get_all_nodes('city'))


class City(Resource):
    def get(self, name):
        return db.get_node('city', 'name', name)


class CityVenues(Resource):
    def get(self, name):
        return db.get_child_nodes('city', 'name', name, 'venue')


class Venues(Resource):
    def get(self):
        return db.get_all_nodes('venue')


class Venue(Resource):
    def get(self, username):
        return db.get_node('venue', 'username', username)


class VenueEvents(Resource):
    def get(self, username):
        return db.get_child_nodes('venue', 'username', username, 'event')


class Event(Resource):
    def get(self, id):
        return db.get_node('event', 'id', id)


class EventBands(Resource):
    def get(self, id):
        return db.get_child_nodes('event', 'id', id, 'band')


class EventVenue(Resource):
    def get(self, id):
        return db.get_child_nodes('event', 'id', id, 'venue')


api.add_resource(Bands, '/bands')
api.add_resource(Band, '/bands/<username>')
api.add_resource(BandEvents, '/bands/<username>/events')
api.add_resource(CityStateList, '/cityStateList')
api.add_resource(Cities, '/cities')
api.add_resource(City, '/cities/<name>')
api.add_resource(CityVenues, '/cities/<name>/venues')
api.add_resource(Venues, '/venues')
api.add_resource(Venue, '/venues/<username>')
api.add_resource(VenueEvents, '/venues/<username>/events')
api.add_resource(Event, '/events/<id>')
api.add_resource(EventVenue, '/events/<id>/venue')
api.add_resource(EventBands, '/events/<id>/bands')


if __name__ == '__main__':
    app.run(port=5002)
