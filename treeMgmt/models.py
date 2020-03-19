# from django.db import models

# Create your models here.
from neo4j import GraphDatabase, basic_auth
from .Tree import Tree
import environ


class GraphConnection(object):

    def __init__(self):
        env = environ.Env(DEBUG=(bool, True))
        # load database enviroment variables
        USER = env('DB_USER')
        PASSWORD = env('DB_PASSWORD')
        DB_URI = env('DB_URI')
        self._driver = GraphDatabase.driver(
            uri=DB_URI, auth=(USER, PASSWORD), encrypted=False)

    def close(self):
        self._driver.close()

    # returns a certain family with a specific lastname
    def get_family(self, last_name):
        with self._driver.session() as session:
            nodes, relations = session.write_transaction(
                self.get_family_nodes, last_name)
            nodeDict = {}
            relationList = []
            for node in nodes:
                nodeDict[node.id] = self.serializePerson(node)
            for relation in relations:
                relationList.append(self.serilatizeRelationship(relation))
            tree = Tree(nodeDict, relationList)
            return tree.jsonTree(tree.root)

        # result = tx.run("MATCH q=(a:Person)-[:CHILD_OF]->(h:Person)-[r:BELONG_TO]->(f:Family{lastName:'Elzohairy'}) return q As persons")

    # run graph query to get family
    @staticmethod
    def get_family_nodes(tx, last_name):
        x = "MATCH p=(a:Person)-[:CHILD_OF]->(b:Person)-[r:BELONG_TO]->(c:Family{{lastName:'{}'}}) return p AS persons UNION MATCH q=(d:Person)-[:MARRIED_TO]->(a) return q AS persons".format(
            last_name)
        print("lalalala", x)
        result = tx.run(
            "MATCH p=(a:Person)-[:CHILD_OF]->(b:Person)-[r:BELONG_TO]->(c:Family{{lastName:'{}'}}) return p AS persons UNION MATCH q=(d:Person)-[:MARRIED_TO]->(a) return q AS persons".format(last_name))
        graph = result.graph()
        nodes = graph.nodes
        relationships = graph.relationships
        dicta = {}
        return nodes, relationships

    # serialize person to node in the graph
    @staticmethod
    def serializePerson(person):
        return {
            'id': person.id,
            'name': person['name'],
            # 'lastname': person['lastname'],
            'gender': person['gender'],
            'age': person['age'],
            'born': person['born']
        }

    # serialize the relation to an edge
    @staticmethod
    def serilatizeRelationship(relation):
        return {
            'id': relation.id,
            # 'role':relation.get('roles')[0],
            'type': relation.type,
            'from': relation.start_node.id,  # child
            'to': relation.end_node.id,  # parent

        }
