class Node:
    def __init__(self, name, function, children = [], leafs = [], parent = None):
        self.name = name
        self.function = function
        self.children = children
        self.leafs = leafs
        self.parent = parent
        self.resolved = False

    def get_name(self):
        return self.name

    def get_function(self):
        return self.function

    def get_children(self):
        return self.children

    def get_leafs(self):
        return self.leafs

    def get_parent(self):
        return self.parent

    def get_ratio(self):
        pass

    def get_leaf_probabilities(self):
        if(self.get_function() == "and"):
            return [leaf.get_probability() for leaf in self.get_leafs()]
        else:
            return [(1-leaf.get_probability()) for leaf in self.get_leafs()]
        
    def get_probability(self):
        if(self.get_function() == "and"):
            return mul(self.get_leaf_probabilities())
        else:
            return 1-mul(self.get_leaf_probabilities())

    def get_cost(self):
        probs = self.get_leaf_probabilities()
        costs = [leaf.get_cost() for leaf in self.get_leafs()]
        cost = 0
        for pos,c in enumerate(costs):
            cost += c * mul([x for x in probs[:pos]])
        return cost

    def set_parent(self, parent):
        self.parent = parent

    def add_child(self, name, function, children = [], leafs = []):
        self.children.append(Node(name, function, children=children, leafs=leafs, parent=self))

    def add_child_node(self, node):
        self.children.append(node)

    def add_leaf(self, name, probability, cost, parent=None):
        self.leafs.append(Leaf(name, probability, cost, parent))

    def add_leaf_node(self, leaf):
        self.leafs.append(leaf)

    def remove_child(self, child):
        return self.children.pop(self.children.index(child))

    def remove_leaf(self, leaf):
        return self.leafs.pop(self.leafs.index(leaf))

    def sort_leafs(self):
        self.leafs.sort(key=lambda leaf:leaf.get_ratio(), reverse=True)

    def is_descendent(self, descendent):
        if(descendent in self.get_children()):
            return True
        for child in self.get_children():
            if(child.is_descendent(descendent)):
                return True
        return False

    def is_resolved(self):
        return self.resolved

    def resolve(self):
        self.resolved = True
    
class Leaf:
    def __init__(self, name, probability, cost, parent = None):
        self.name = name
        self.probability = probability
        self.cost = cost
        self.parent = parent

    def get_name(self):
        return self.name

    def get_probability(self):
        return self.probability

    def get_cost(self):
        return self.cost

    def get_children(self):
        return []

    def get_parent(self):
        return self.parent

    def get_ratio(self):
        if(self.get_parent().get_function() == "or"):
            return self.probability/self.cost
        else:
            return (1-self.probability)/self.cost

    def set_probability(self, p):
        self.probability = p

    def set_cost(self, c):
        self.cost = c

    def set_parent(self, parent):
        self.parent = parent

names = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def get_name():
    return names.pop(0)

def mul(lis):
    prod = 1
    for x in lis:
        prod *= x
    return prod

def create_tree(expression, nodes=[], root=True, vals=None):
    if not(expression):
        expression = input("Enter a boolean expression: ")
    while("(" in expression):
        a = expression.index("(")
        b = a
        counter = 1
        while(counter > 0):
            b += 1
            if(expression[b] == "("):
                counter += 1
            elif(expression[b] == ")"):
                counter -= 1
        nodes.append(create_tree(expression[a+1:b], root=False))
        expression = expression[:a] + str(len(nodes)-1) + expression[b+1:]
    if("|" in expression):
        parts = expression.split("|")
        node = Node(get_name(), "or",
                    children=[create_tree(x, nodes, root=False) for x in parts if (x.isdigit())],
                    leafs=[Leaf(x, 0, 0) for x in parts if (not(x.isdigit()))])
    elif("&" in expression):
        parts = expression.split("&")
        node = Node(get_name(), "and",
                    children=[nodes[int(x)] for x in parts if x.isdigit()],
                    leafs=[Leaf(x, 0, 0) for x in parts if not(x.isdigit())])
    else:
        node = nodes[int(expression)]

    if(root):
        fix_tree(node)
        simplify_tree(node)
        set_leafs(node, vals)
        print_tree(node)
        
    return node

def fix_tree(node):
    for child in node.get_children():
        child.set_parent(node)
        fix_tree(child)
    for leaf in node.get_leafs():
        leaf.set_parent(node)

def simplify_tree(node):
    remove = []
    for child in node.get_children():
        simplify_tree(child)
        if(child.get_function() == node.get_function()):
            for grandchild in child.get_children():
                node.add_child_node(grandchild)
            for grandleaf in child.get_leafs():
                node.add_leaf_node(grandleaf)
            remove.append(child)
    for r in remove:
        node.remove_child(r)

def set_leafs(node, vals=None):
    if(vals):
        for leaf in node.get_leafs():
            leaf.set_probability(vals.get(leaf.get_name()).get("probability"))
            leaf.set_cost(vals.get(leaf.get_name()).get("cost"))
        for child in node.get_children():
            set_leafs(child, vals)
    else:
        for leaf in node.get_leafs():
            print("Leaf {}".format(leaf.get_name()))
            print("Enter probability (currently {}): ".format(leaf.get_probability()), end="")
            leaf.set_probability(float(input()))
            print("Enter cost (currently {}): ".format(leaf.get_cost()), end="")
            leaf.set_cost(float(input()))
        for child in node.get_children():
            set_leafs(child)

def print_tree(node, depth=0):
    print("-"*depth + "{} {}".format(node.get_name(), node.get_function()))
    for leaf in node.get_leafs():
        print("-"*(depth+1) + "{} p={} c={} r={}".format(leaf.get_name(), round(leaf.get_probability(),3), round(leaf.get_cost(),3), round(leaf.get_ratio(),3)))
    for child in node.get_children():
        print_tree(child, depth+1)
