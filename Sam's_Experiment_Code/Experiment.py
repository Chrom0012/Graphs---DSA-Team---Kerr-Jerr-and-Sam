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

print(Graph['A'])  # Output: ['B', 'C']
print(Graph['B'])  # Output: ['A', 'D', 'E']