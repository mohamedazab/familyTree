def createFamilyNode(tx, attributesDict):
    return tx.run("CREATE (f:Family{id:$id, lastName:$family }) RETURN f.id", attributesDict).single().value()


def createPersonNode(tx, attributesDict):
    return tx.run("CREATE (newNode:Person {id:$id,name:$name,age:$age,born:$born,gender:$gender}) RETURN newNode.id", attributesDict).single().value()


# get node by ID
def getPersonNodeById(tx, attributesDict):
    return tx.run("Match (p:Person{id:$id}) return p.id", attributesDict['id']).single().value()

# create BELONG_TO relation


def createBelongToRelation(tx, attributesDict):
    print(attributesDict['childId'])
    print(attributesDict['parentId'])
    tx.run(
        "match(child:Person) where child.id = $childId match(parent:Family) where parent.id = $parentId create(child)-[:BELONG_TO]->(parent)", childId=attributesDict['childId'], parentId=attributesDict['parentId'])

# create CHILD_OF RELATION

# add leaf to the tree
def createChildOfRelation(tx, attributesDict):
    tx.run(
        "match(child:Person) where child.id = $childId match(parent:Person) where parent.id = $parentId create(child)-[:CHILD_OF {roles:[child.gender]}]->(parent)", childId=attributesDict['childId'], parentId=attributesDict['parentId'])


# make all children grand children. make new node child for these children add middle node
def addOnlyChild(tx, attributesDict):
    tx.run(
        "MATCH p=(y:Person)-[r:CHILD_OF]->(x:Person{id:$parentId})  MATCH q=(n:Person{id:$childID}) delete r CREATE (y)-[m:CHILD_OF {roles:[y.gender]}]->(n)", attributesDict)


