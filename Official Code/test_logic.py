from logic import graph

Graph = graph()
Graph.add_edge('A', 'B')
Graph.add_edge('A', 'C')
print("Map of the graph:")
for node, edges in Graph.graph.items():
    print(f"Node {node} is connected to {edges}")
