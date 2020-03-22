
def serializePerson(person):
    return {
        'id': person['id'],
        'name': person['name'],
        # 'lastname': person['lastname'],
        'gender': person['gender'],
        'age': person['age'],
        'born': person['born']
    }

# serialize the relation to an edge


def serilatizeRelationship(relation):
    return {
        'id': relation.id,
        # 'role':relation.get('roles')[0],
        'type': relation.type,
        'from': relation.start_node.id,  # child
        'to': relation.end_node.id,  # parent

    }
