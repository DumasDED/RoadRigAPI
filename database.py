from py2neo import Graph, Node, Relationship

import config
import error

try:
    db = Graph(password=config.db_password)
except error.types as e:
    error.handle(e)


def get_node(label, key, value):
    node = db.find_one(label, key, value)
    return node


def get_child_nodes(parent_label, key, value, child_label):
    nodes = db.data("match (a:%s)-[]-(b:%s) where a.%s = '%s' return b" % (parent_label, child_label, key, value))
    nodes = [node['b'] for node in nodes]
    return nodes


def get_all_nodes(label):
    nodes = db.find(label)
    return nodes


def get_related_nodes(left_label, right_label):
    nodes = db.data("match ({0}:{0})-[]-({1}:{1}) return {0}, {1}".format(left_label, right_label))
    return nodes