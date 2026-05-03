class graph:
    def __init__(self):
        self.graph = {}
    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []
    def add_edge(self, node1, node2):
        self.add_node(node1)
        self.add_node(node2)
        if node2 not in self.graph[node1]:
            self.graph[node1].append(node2)
        if node1 not in self.graph[node2]:
            self.graph[node2].append(node1)
    def BFS(self, start):
        visited = []
        queue = [start]
        Steps = 0
        Path = 0
        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.append(node)
                Steps += 1
                for edge in self.graph[node]:
                    Steps += 1
                    if edge not in visited:
                        Path += 1
                        queue.append(edge)
        return visited, Steps, Path