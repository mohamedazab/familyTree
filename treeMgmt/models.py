# from django.db import models

# Create your models here.
from neo4j import GraphDatabase
from .Tree import Tree

class Graph(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    # returns a certain family with a specific lastname
    def get_family(self, last_name):
        with self._driver.session() as session:
            nodes,relations = session.write_transaction(self.get_family_nodes, last_name)
            nodeDict = {}
            relationList = []
            for node in nodes:
                nodeDict[node.id]=self.serializePerson(node)
            for relation in relations:
                relationList.append(self.serilatizeRelationship(relation))
            tree = Tree(nodeDict,relationList)
            print(tree.jsonTree(tree.root))


        # result = tx.run("MATCH q=(a:Person)-[:CHILD_OF]->(h:Person)-[r:BELONG_TO]->(f:Family{lastName:'Elzohairy'}) return q As persons")

    # run graph query to get family
    @staticmethod
    def get_family_nodes(tx, lastname):
        result = tx.run("MATCH p=(a:Person)-[:CHILD_OF]->(b:Person)-[r:BELONG_TO]->(c:Family{lastName:'{}'}) return p AS persons UNION MATCH q=(d:Person)-[:MARRIED_TO]->(a) return q AS persons".format(lastname))
        graph = result.graph()
        nodes = graph.nodes
        relationships = graph.relationships
        dicta = {}
        return nodes,relationships

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
            'id':relation.id,
            # 'role':relation.get('roles')[0],
            'type':relation.type,
            'from': relation.start_node.id, #child
            'to': relation.end_node.id, #parent

        }
