from collections import defaultdict


class Tree(object):
    def __init__(self, nodes, relations):

        # dict mapping node id to node
        self.nodes = nodes
        # list of relations
        self.relations = relations
        self.root = None
        # dict mapping node id to its full children nodes
        self.children = defaultdict(lambda: [])
        # dict mapping node id to its mates (full node)
        self.mates = defaultdict(lambda: None)
        for relation in self.relations:
            if relation['type'] == "BELONG_TO": # 1 BELONG_TO to determine root
                self.root = self.nodes[relation['from']]
            elif(relation['type'] == "CHILD_OF"): # multiple children
                self.children[relation['to']].append(
                    self.nodes[relation['from']])
            elif(relation['type'] == "MARRIED_TO"): # only one married to relation
                self.mates[relation['to']]=self.nodes[relation['from']]
        # print("got root", self.root)
        # print(" chidren ", self.children)
        # print("mates:", self.mates)
        # print(self.relations)

    def jsonTree(self, root):
        if root == None:
            return []
        children = self.children[root['id']]
        result = {}
        result['node'] = root
        result['mate'] = self.mates[root['id']]
        result['children'] = []
        for node in children:
            ans = self.jsonTree(node)
            result['children'].append(ans)
        return result
