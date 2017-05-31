import tree
from tree import mul
import copy
import random

class StrategyNode:
    def __init__(self, name):
        self.name = name
    
def create_output(node, output, depth, path):
    if(len(output) <= depth):
        output.append(["-" for x in range(2**depth)])
    output[depth][int("0"+path,2)] = node.name
    if(node.true):
        output = create_output(node.true, output, depth+1, path+"1")
        output = create_output(node.false, output, depth+1, path+"0")
    return output

def twin_simplify(root):
    classes = {}
    for leaf in root.get_leafs():
        ratio = round(leaf.get_ratio(),4)
        if(ratio in classes):
            classes.get(ratio).append(leaf)
        else:
            classes.update({ratio:[leaf]})
    for r in classes:
        rclass = classes.get(r)
        if(len(rclass) > 1):
            if(root.get_function() == "or"):
                prob = 1-mul([1-leaf.get_probability() for leaf in rclass])
                cost = prob/r
            else:
                prob = mul([leaf.get_probability() for leaf in rclass])
                cost = (1-prob)/r
            name = ''.join([leaf.get_name() for leaf in rclass])
            root.add_leaf(name, prob, cost, parent=root)
            for leaf in rclass:
                root.remove_leaf(leaf)
    for child in root.get_children():
        twin_simplify(child)

def create_tuple(root):
    sizes = ()
    nodes = ()
    if(len(root.get_leafs()) > 0):
        sizes += (len(root.get_leafs()),)
        nodes += (root,)
    for child in root.get_children():
        s,n = create_tuple(child)
        sizes += s
        nodes += n
    return sizes, nodes

def generate_tuples(num_tests, tup, start=()):
    if (len(start) == len(tup)-1):
        if(num_tests-sum(start) > tup[-1]):
            return []
        else:
            return [start + (num_tests-sum(start),)]
    tuples = []
    for next_val in range(min(num_tests - sum(start) + 1, tup[len(start)] + 1)):
        tuples += generate_tuples(num_tests, tup, start + (next_val,))
    return tuples

def short(sizes, node, nodes):
    if not(node.get_parent()):
        return [0 for x in sizes]
    if node in nodes:
        sizes[nodes.index(node)] = 0
    parent = node.get_parent()
    resolved = not(parent in nodes) or (sizes[nodes.index(parent)] == 0)
    for pos,n in enumerate(nodes):
        if node.is_descendent(n):
            sizes[pos] = 0
        elif resolved and sizes[pos] != 0 and parent.is_descendent(n):
            resolved = False

    if resolved:
        if not(parent.get_parent()):
            return [0 for x in sizes]
        return short(sizes, parent.get_parent(), nodes)

    return sizes

def run(root=None, expression=None, vals=None, out=False):
    if not(expression) and not(root):
        random.seed(100)
        vals = {x:{"probability":random.random(), "cost":random.random()}
                for val,x in enumerate("abcdefghijklmnopqrstuvwxyz")}

        expression = "a|(b&c&(d|e|(f&g))&(h|i))|(j&k&l&(m|n|((o|p)&(q|r))))"
        expression = "(((a|b)&(c|d))|((e|f)&(g|h)))&(((i|j)&(k|l))|((m|n)&(o|p)))"
        
        print("Original Tree: ")
        root = tree.create_tree(expression, vals=vals)

    root = copy.deepcopy(root)
    
    twin_simplify(root)

    if out:
        print("Simplified Tree: ")
        tree.print_tree(root)

        
    tup = create_tuple(root)

    cost = {tuple(0 for node in tup[1]): 0}
    first_test = {(0 for node in tup[1]): None}
    true_arc = {}
    false_arc = {}
    for num_tests in range(1,sum(tup[0])+1):
        for reduced_tuple in generate_tuples(num_tests, tup[0]):
            for class_size, sibling_class in zip(reduced_tuple, tup[1]):
                if(class_size > 0):
                    sibling_class.sort_leafs()
                    leaf = sibling_class.get_leafs()[-class_size]
                    i_pos = list(reduced_tuple)
                    i_neg = list(reduced_tuple)

                    i_pos = short(i_pos, sibling_class, tup[1])
                    i_neg[tup[1].index(sibling_class)] -= 1
                    resolved = class_size == 1
                    for pos,n in enumerate(tup[1]):
                        if resolved and reduced_tuple[pos] != 0 and sibling_class.is_descendent(n):
                            resolved = False

                    if resolved:
                        if not(sibling_class.get_parent()):
                            i_neg = [0 for x in tup[1]]
                        else:
                            i_neg = short(i_neg, sibling_class.get_parent(), tup[1])
                        
                    
                    i_pos = tuple(i_pos)
                    i_neg = tuple(i_neg)
                    if(sibling_class.get_function() == "and"):
                        i_pos, i_neg = i_neg, i_pos        
                    c = leaf.get_cost() + leaf.get_probability()*cost.get(i_pos) + (1-leaf.get_probability())*cost.get(i_neg)
                    if(not(reduced_tuple in cost) or c < cost.get(reduced_tuple)):
                        cost.update({reduced_tuple:c})
                        first_test.update({reduced_tuple:leaf})
                        true_arc.update({reduced_tuple:i_pos})
                        false_arc.update({reduced_tuple:i_neg})

    print("Cost: " + str(round(cost.get(tup[0]),7)))

    def create_strategy(tup, value="F"):
        if([x for x in tup if x > 0]):
            node = StrategyNode(first_test.get(tup).get_name())
            node.true = create_strategy(true_arc.get(tup), "T")
            node.false = create_strategy(false_arc.get(tup), "F")
        else:
            node = StrategyNode(value)
            node.true = None
            node.false = None
        return node
    output = create_output(create_strategy(tup[0]), [], 0, "")

    if out:
        width = 2**(len(tup[0])+1)-1
        for pos,line in enumerate(output, start=1):
            layer = len(output)-pos
            print(" "*(2**layer-1)+( " " * (2**(layer+1)-1)).join(line))

    return output

