import time
import random
import tree
import DynProg
import DFA

random.seed(100)
vals = {x:{"probability":random.random(), "cost":random.random()}
        for val,x in enumerate("abcdefghijklmnopqrstuvwxyz")}

expression = "a|(b&c&(d|e|(f&g))&(h|i))|(j&k&l&(m|n|((o|p)&(q|r))))"
expression = "(((a|b)&(c|d))|((e|f)&(g|h)))&(((i|j)&(k|l))|((m|n)&(o|p)))"


print("Tree:")
root = tree.create_tree(expression, vals=vals)

start = time.time()
print("\nRunning DynProg...")
DynProg.run(root=root)
print("Time Taken: {} seconds".format(time.time()-start))

start = time.time()
print("\nRunning DFA...")
DFA.run(root=root)
print("Time Taken: {} seconds".format(time.time()-start))

