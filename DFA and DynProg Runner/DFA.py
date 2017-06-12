import tree
import copy
import random

def reduce(root):
    for child in root.get_children():
        root.add_leaf_node(reduce(child))
    for child in root.get_children():
        root.remove_child(child)
    root.sort_leafs()
    name = "".join([leaf.get_name() for leaf in root.get_leafs()])
    probability = root.get_probability()
    cost = root.get_cost()
    return tree.Leaf(name, probability, cost, parent=root.get_parent())

def run(root=None, expression=None, vals=None, out=False):
    leaf = reduce(copy.deepcopy(root))
    return leaf.get_cost()
    print("Strategy: {}".format(leaf.get_name()))
    print("Cost: {}".format(round(leaf.get_cost(),7)))
    print("Probability: {}".format(round(leaf.get_probability(),7)))
