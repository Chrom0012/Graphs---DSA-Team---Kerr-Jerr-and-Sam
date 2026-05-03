from logic import graph

Graph = graph()

while True:
    Input = input("Enter a command (node, edge, BFS, or 0 to exit): ")
    if Input == "node":
        node = input("Enter the node to add: ")
        Graph.add_node(node)
        print(f"Node {node} added.")
    elif Input == "edge":
        node1 = input("Enter the first node: ")
        node2 = input("Enter the second node: ")
        Graph.add_edge(node1, node2)
        print(f"Edge between {node1} and {node2} added.")
    elif Input == "BFS":
        start = input("Enter the starting node for BFS: ")
        visited, Steps = Graph.BFS(start)
        print(f"Visited nodes: {visited}")
        print(f"Total steps taken: {Steps}")
    elif Input == "0":
        break
    else:
        print("Invalid command. Please try again.")

print("Map of the graph:")
for node, edges in Graph.graph.items():
    print(f"Node {node} is connected to {edges}")
