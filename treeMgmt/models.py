# from django.db import models

# Create your models here.
from neo4j import GraphDatabase
from .Tree import Tree

class Graph(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    # def print_greeting(self, message):
    #     with self._driver.session() as session:
    #         greeting = session.write_transaction(
    #             self._create_and_return_greeting, message)
    #         print(greeting)

    # @staticmethod
    # def _create_and_return_greeting(tx, message):
    #     result = tx.run("CREATE (a:Greeting) "
    #                     "SET a.message = $message "
    #                     "RETURN a.message + ', from node ' + id(a)", message=message)
    #     return result.single()[0]

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

    @staticmethod
    def get_family_nodes(tx, lastname):
        result = tx.run("MATCH p=(a:Person)-[:CHILD_OF]->(b:Person)-[r:BELONG_TO]->(c:Family{lastName:'Elzohairy'}) return p AS persons UNION MATCH q=(d:Person)-[:MARRIED_TO]->(a) return q AS persons")
        graph = result.graph()
        nodes = graph.nodes
        relationships = graph.relationships
        dicta = {}
        return nodes,relationships

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

    @staticmethod # where role is son or daughter
    def serilatizeRelationship(relation):
        return { 
            'id':relation.id,
            # 'role':relation.get('roles')[0],
            'type':relation.type,
            'from': relation.start_node.id, #child
            'to': relation.end_node.id, #parent

        }
