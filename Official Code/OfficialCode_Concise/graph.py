# graph.py - Pure Graph Data Structure
print("=== graph.py LOADED ===")

class Graph:
    def __init__(self):
        self.adj_list = {}   # {vertex: [(neighbor, edge_canvas_id), ...]}

    def add_vertex(self, v):
        if v not in self.adj_list:
            self.adj_list[v] = []

    def add_edge(self, v1, v2, edge_id=None):
        self.add_vertex(v1)
        self.add_vertex(v2)
        if v2 not in [n for n, _ in self.adj_list[v1]]:
            self.adj_list[v1].append((v2, edge_id))
        if v1 not in [n for n, _ in self.adj_list[v2]]:
            self.adj_list[v2].append((v1, edge_id))

    def get_neighbors(self, v):
        return self.adj_list.get(v, [])