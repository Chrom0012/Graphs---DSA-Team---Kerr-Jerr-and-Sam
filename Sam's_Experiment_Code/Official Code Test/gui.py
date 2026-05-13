# gui.py
from logic import graph

mode = "idle"
node_count = 0

nodes = {}
selected_nodes = []

canvas = None
status_label = None
hint_label = None

# ================= GRAPH =================

g = graph()

# ================= VISUAL SETTINGS =================

NODE_RADIUS = 20

DEFAULT_NODE_COLOR = "white"
HIGHLIGHT_NODE_COLOR = "#d9d9d9"

DEFAULT_TEXT_COLOR = "black"

EDGE_COLOR = "white"

# ================= STORAGE =================

node_visuals = {}

# ================= UI REFERENCES =================

def set_ui_refs(c, status, hint):
    global canvas, status_label, hint_label

    canvas = c
    status_label = status
    hint_label = hint

# ================= HELPERS =================

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

    elif mode == "bfs":
        status_label.config(text="Status: BFS Traversal")
        update_hint("Click a starting node")

    elif mode == "dfs":
        status_label.config(text="Status: DFS Traversal")
        update_hint("Click a starting node")

    else:
        status_label.config(text="Status: Idle")
        update_hint("Select a mode to begin")

# ================= BUTTON MODES =================

def toggle_node():
    set_mode("idle" if mode == "node" else "node")

def toggle_edge():
    set_mode("idle" if mode == "edge" else "edge")

def toggle_bfs():
    set_mode("idle" if mode == "bfs" else "bfs")

def toggle_dfs():
    set_mode("idle" if mode == "dfs" else "dfs")

# ================= RESET =================

def reset_graph():
    global node_count

    canvas.delete("all")

    nodes.clear()
    selected_nodes.clear()
    node_visuals.clear()

    g.graph.clear()

    node_count = 0

    set_mode("idle")

# ================= NODE DETECTION =================

def get_clicked_node(x, y):

    for nid, (nx, ny) in nodes.items():

        if (x - nx) ** 2 + (y - ny) ** 2 <= NODE_RADIUS ** 2:
            return nid

    return None

# ================= HOVER EFFECT =================

def hover_highlight_node(event):

    x, y = event.x, event.y

    hovered = get_clicked_node(x, y)

    for nid, visuals in node_visuals.items():

        oval_id = visuals["oval"]

        if nid == hovered:
            canvas.itemconfig(
                oval_id,
                fill=HIGHLIGHT_NODE_COLOR
            )

        else:
            canvas.itemconfig(
                oval_id,
                fill=DEFAULT_NODE_COLOR
            )

# ================= MAIN CLICK =================

def on_canvas_click(event):

    global node_count

    x, y = event.x, event.y

    # ================= ADD NODE =================

    if mode == "node":

        oval = canvas.create_oval(
            x - NODE_RADIUS,
            y - NODE_RADIUS,
            x + NODE_RADIUS,
            y + NODE_RADIUS,
            fill=DEFAULT_NODE_COLOR,
            outline=""
        )

        text = canvas.create_text(
            x,
            y,
            text=str(node_count),
            fill=DEFAULT_TEXT_COLOR
        )

        nodes[node_count] = (x, y)

        node_visuals[node_count] = {
            "oval": oval,
            "text": text
        }

        g.add_node(node_count)

        node_count += 1

    # ================= ADD EDGE =================

    elif mode == "edge":

        clicked = get_clicked_node(x, y)

        if clicked is None:
            return

        if len(selected_nodes) == 1 and selected_nodes[0] == clicked:
            return

        selected_nodes.append(clicked)

        if len(selected_nodes) == 1:
            update_hint("Click the second node")

        if len(selected_nodes) == 2:

            n1 = selected_nodes[0]
            n2 = selected_nodes[1]

            x1, y1 = nodes[n1]
            x2, y2 = nodes[n2]

            canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill=EDGE_COLOR,
                width=2
            )

            g.add_edge(n1, n2)

            selected_nodes.clear()

            update_hint("Click the first node")

    # ================= BFS =================

    elif mode == "bfs":

        clicked = get_clicked_node(x, y)

        if clicked is None:
            return

        visited, steps, path = g.BFS(clicked)

        status_label.config(
            text=f"BFS: {visited}"
        )

        update_hint(
            f"Steps: {steps} | Paths: {path}"
        )

    # ================= DFS =================

    elif mode == "dfs":

        clicked = get_clicked_node(x, y)

        if clicked is None:
            return

        visited, steps, path = g.DFS(clicked)

        status_label.config(
            text=f"DFS: {visited}"
        )

        update_hint(
            f"Steps: {steps} | Paths: {path}"
        )