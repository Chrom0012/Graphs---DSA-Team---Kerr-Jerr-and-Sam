# Example kunyare ng nodes and edges
Graph = {
    'A' : ['B', 'C'],
    'B' : ['A', 'D', 'E'],
    'C' : ['A', 'F'],
    'D' : ['B'],
    'E' : ['B'],
    'F' : ['C']
}
# 'A' is the node, whereas 'B' and 'C' is mga edges na connected kay 'A'.
# Example this ng Adjacency list. 
print(Graph['A'])  # ['B', 'C']
print(Graph['B'])  # ['A', 'D', 'E']
print(Graph['C'])  # ['A', 'F']

""" If I-traverse natin s'ya
for i in Graph:
    print(i, Graph[i])
"""


for i in Graph.items():
    print(i)