# from django.db import models

# Create your models here.
from neo4j import GraphDatabase, CypherError
from .Tree import Tree
import environ
from .serializer import serializePerson, serilatizeRelationship
import json

from .transactions import *


class GraphConnection(object):

    def __init__(self):
        env = environ.Env(DEBUG=(bool, True))
        # load database enviroment variables
        USER = env('DB_USER')
        PASSWORD = env('DB_PASSWORD')
        DB_URI = env('DB_URI')
        print(DB_URI)
        self._driver = GraphDatabase.driver(
            uri=DB_URI, auth=(USER, PASSWORD), encrypted=False)

    def close(self):
        self._driver.close()

    # returns a certain family with a specific lastname
    def getFamily(self, attributesDict):
        with self._driver.session() as session:
            result = {}
            try:
                print(attributesDict)
                resultStatment = session.run(
                    "MATCH p=(a:Person)-[:CHILD_OF]->(b:Person)-[r:BELONG_TO]->(c:Family{lastName:$family}) return p AS persons UNION MATCH q=(d:Person)-[:MARRIED_TO]->(a) return q AS persons ", attributesDict)
                graph = resultStatment.graph()
                nodes = graph.nodes
                relations = graph.relationships
                nodeDict = {}
                relationList = []
                for node in nodes:
                    nodeDict[node.id] = serializePerson(node)
                for relation in relations:
                    relationList.append(serilatizeRelationship(relation))
                tree = Tree(nodeDict, relationList)
                result['success'] = True
                result['data'] = tree.jsonTree(tree.root)
            except CypherError:
                result['success'] = "can not get family tree!"
            return result

    # add family with last name
    def addFamily(self, attributesDict):
        result = {}
        with self._driver.session() as session:
            try:
                tx = session.begin_transaction()
                familyId = createFamilyNode(tx,attributesDict)
                print("family id",familyId)
                tx.commit()
                result['success'] = True
            except CypherError:
                result['success'] = "family last name must be unique"
            return result

    def addMainNode(self,attributesDict):
        parentId = attributesDict['parentId']
        newNode = attributesDict['newNode']
        result = {}
        print("got parent id",parentId)
        print("got new node", newNode)
        with self._driver.session() as session:
            try:

                tx = session.begin_transaction()
                newNodeId = createPersonNode(tx,newNode)
                print(newNodeId)
                createBelongToRelation(tx,{'childId':newNodeId,'parentId':parentId})
                tx.commit()
                print("success",tx.success)
                result['success'] = True
            except CypherError:
                result['success'] = 'error can not add this family member please try again'
            return result

    # add node
    def addNode(self, attributesDict):
        parentId = attributesDict['parentId']
        newNode = attributesDict['newNode']
        result = {}
        with self._driver.session() as session:
            try:

                tx = session.begin_transaction()
                newNodeId = createPersonNode(tx,newNode)
                print(newNodeId)
                createChildOfRelation(tx,{'childId':newNodeId,'parentId':parentId})
                print("success",tx.success)
                result['success'] = True
                tx.commit()
                print(tx.success)
                result['success'] = True
            except CypherError:
                result['success'] = 'error can not add this family member please try again'
            return result

