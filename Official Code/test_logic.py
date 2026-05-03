from logic import graph

Graph = graph()

while True:
    input = input("Enter a command (node, edge, or 0 to exit): ")
    if input == "node":
        node = input("Enter the node to add: ")
        Graph.add_node(node)
        print(f"Node {node} added.")
    elif input == "edge":
        node1 = input("Enter the first node: ")
        node2 = input("Enter the second node: ")
        Graph.add_edge(node1, node2)
        print(f"Edge between {node1} and {node2} added.")
    elif input == "0":
        break
    else:
        print("Invalid command. Please try again.")

print("Map of the graph:")
for node, edges in Graph.graph.items():
    print(f"Node {node} is connected to {edges}")
