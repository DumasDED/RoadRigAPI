from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api

# TODO: get rid of database, incorporate all calls directly
import database as db

from py2neo import Graph, Node, Relationship

import config
import error

app = Flask(__name__)
CORS(app)
api = Api(app)

try:
    db_direct = Graph(password=config.db_password)
except error.types as e:
    error.handle(e)


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
        nodes = db_direct.data("""
            match (b:band)-[]-(e:event)-[]-(n:venue)-[]-(c:city)
            where c.name = '%s'
            return n, count(e) as events, count(distinct b) as bands
            order by count(e) desc""" % name)
        nodes = [n['n'] for n in nodes]
        return nodes


class Venues(Resource):
    def get(self):
        return db.get_all_nodes('venue')


class Venue(Resource):
    def get(self, username):
        return db.get_node('venue', 'username', username)


class VenueEvents(Resource):
    def get(self, identifier):
        nodes = db_direct.data("""
            match (e:event)-[]-(v:venue)
            where v.%s= '%s'
            return e""" % (search_by(identifier), identifier))
        return nodes


class VenueBands(Resource):
    def get(self, identifier):
        nodes = db_direct.data("""
            match (b:band)-[]-(e:event)-[]-(v:venue)
            where v.%s= '%s'
            return b""" % (search_by(identifier), identifier))
        return nodes


class Event(Resource):
    def get(self, id):
        return db.get_node('event', 'id', id)


class EventBands(Resource):
    def get(self, id):
        return db.get_child_nodes('event', 'id', id, 'band')


class EventVenue(Resource):
    def get(self, id):
        return db.get_child_nodes('event', 'id', id, 'venue')


def search_by(searchvalue):
    try:
        float(searchvalue)
        return 'id'
    except ValueError:
        return 'username'

api.add_resource(Bands, '/bands')
api.add_resource(Band, '/bands/<username>')
api.add_resource(BandEvents, '/bands/<username>/events')
api.add_resource(CityStateList, '/cityStateList')
api.add_resource(Cities, '/cities')
api.add_resource(City, '/cities/<name>')
api.add_resource(CityVenues, '/cities/<name>/venues')
api.add_resource(Venues, '/venues')
api.add_resource(Venue, '/venues/<username>')
api.add_resource(VenueEvents, '/venues/<identifier>/events')
api.add_resource(VenueBands, '/venues/<identifier>/bands')
api.add_resource(Event, '/events/<id>')
api.add_resource(EventVenue, '/events/<id>/venue')
api.add_resource(EventBands, '/events/<id>/bands')


if __name__ == '__main__':
    app.run(port=5002)
