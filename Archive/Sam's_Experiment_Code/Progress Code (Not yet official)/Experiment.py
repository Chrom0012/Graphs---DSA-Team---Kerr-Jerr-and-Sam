Graph = {
    'A' : ['B', 'C'],
    'B' : ['A', 'D', 'E'],
    'C' : ['A', 'F'],
    'D' : ['B'],
    'E' : ['B'],
    'F' : ['C']
}
print(Graph['A'])  # ['B', 'C']
print(Graph['B'])  # ['A', 'D', 'E']
print(Graph['C'])  # ['A', 'F']


for i in Graph.items():
    print(i)
