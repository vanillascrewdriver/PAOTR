import time
import random
import tree
import DynProg
import DFA

def run(expression):
    random.seed(300)
    a = expression.replace("(",",").replace(")",",").replace("|",",").replace("&",",")
    vals = {x:{"probability":random.random(), "cost":random.random()} for x in a.split(",")}

    print("Tree:")
    root = tree.create_tree(expression, vals=vals)

    start = time.time()
    print("\nRunning DynProg...")
    r = DynProg.run(root=root, expression=expression, vals=vals)
    print("Time Taken: {} seconds".format(time.time()-start))

    start = time.time()
    print("\nRunning DFA...")
    DFA.run(root=root, expression=expression, vals=vals)
    print("Time Taken: {} seconds".format(time.time()-start))

