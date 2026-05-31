from graph import Graph   

pending_algorithm = None      
last_start_vertex = None
last_algorithm = None         
graph_instance = Graph()   
vertex_items = {}

mode = "idle"
node_count = 0
nodes = {}
selected_nodes = []

canvas = None
status_label = None
hint_label = None

root = None

def set_ui_refs(c, status, hint, root_window):
    global canvas, status_label, hint_label, root, pending_algorithm
    canvas = c
    status_label = status
    hint_label = hint
    root = root_window
    pending_algorithm = None   


def update_hint(text):
    if hint_label:
        hint_label.config(text=text)


def set_mode(new_mode):
    global mode, selected_nodes

    mode = new_mode
    selected_nodes = []

    if mode == "node":
        status_label.config(text="Status: Add Node Mode")
        update_hint("Click anywhere on the canvas to add a node")

    elif mode == "edge":
        status_label.config(text="Status: Add Edge Mode")
        update_hint("Click the first node")

    else:
        status_label.config(text="Status: Idle")
        update_hint("Select a mode to begin")


def toggle_node():
    set_mode("idle" if mode == "node" else "node")


def toggle_edge():
    set_mode("idle" if mode == "edge" else "edge")


def on_canvas_click(event):
    global node_count, selected_nodes, pending_algorithm, last_start_vertex, last_algorithm
    x, y = event.x, event.y

    # === NEW: Click-to-start traversal mode (exactly like classmate's video) ===
    if pending_algorithm:
        # Check if user clicked a vertex
        for vid, data in list(vertex_items.items()):
            nx, ny = data["pos"]
            if (x - nx)**2 + (y - ny)**2 <= 400:   # click tolerance
                start = vid
                last_start_vertex = start
                last_algorithm = pending_algorithm

                if pending_algorithm == "BFS":
                    visited, steps, path = graph_instance.BFS(start)
                    status_label.config(text=f"BFS Complete | Steps: {steps} | Path: {path}")
                    hint_label.config(text=f"Visited: {visited}")
                else:  # DFS
                    visited, steps, path = graph_instance.DFS(start)
                    status_label.config(text=f"DFS Complete | Steps: {steps} | Path: {path}")
                    hint_label.config(text=f"Visited: {visited}")

                animate_traversal(visited, speed_ms=400)
                pending_algorithm = None   # exit selection mode
                return
        return   # clicked empty space → do nothing

    # === Existing code for Add Vertex / Add Edge modes ===
    if mode == "node":
        r = 20
        oval_id = canvas.create_oval(x - r, y - r, x + r, y + r,
                                     fill="white", outline="black", width=2)
        text_id = canvas.create_text(x, y, text=str(node_count),
                                     fill="black", font=("42dot Sans", 14, "bold"))
        vertex_items[node_count] = {"oval": oval_id, "text": text_id, "pos": (x, y)}
        graph_instance.add_vertex(node_count)
        node_count += 1
        update_hint(f"Vertex {node_count-1} added")

    elif mode == "edge":
        for nid, data in list(vertex_items.items()):
            nx, ny = data["pos"]
            if (x - nx)**2 + (y - ny)**2 <= 400:
                if len(selected_nodes) == 1 and selected_nodes[0] == nid:
                    return
                selected_nodes.append(nid)

                if len(selected_nodes) == 1:
                    update_hint("Click the second vertex")
                elif len(selected_nodes) == 2:
                    v1 = selected_nodes[0]
                    v2 = selected_nodes[1]
                    n1 = vertex_items[v1]["pos"]
                    n2 = vertex_items[v2]["pos"]
                    canvas.create_line(n1[0], n1[1], n2[0], n2[1],
                                       fill="#a8a8a8", width=3, tags="edge")
                    graph_instance.add_edge(v1, v2)
                    selected_nodes.clear()
                    update_hint("Click first vertex for next edge")
                break

def animate_traversal(visit_order, speed_ms=300):
    def highlight_step(i):
        global root
        if i < len(visit_order):
            vid = visit_order[i]
            if vid in vertex_items:
                canvas.itemconfig(vertex_items[vid]["oval"], fill="#ffd700")  
                canvas.itemconfig(vertex_items[vid]["text"], fill="black")
            root.after(speed_ms, lambda: highlight_step(i + 1))  
        else:
            for vid in visit_order:
                if vid in vertex_items:
                    canvas.itemconfig(vertex_items[vid]["oval"], fill="#00ff88")  
    highlight_step(0)
