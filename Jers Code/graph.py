# ================= GRAPH LOGIC =================
mode = "idle"
node_count = 0
nodes = {}
selected_nodes = []

# UI references
canvas = None
status_label = None
hint_label = None


def set_ui_refs(c, status, hint):
    global canvas, status_label, hint_label
    canvas = c
    status_label = status
    hint_label = hint


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
    global node_count

    x, y = event.x, event.y

    # ================= NODE MODE =================
    if mode == "node":
        r = 20

        canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill="white",
            outline=""
        )

        canvas.create_text(x, y, text=str(node_count), fill="black")

        nodes[node_count] = (x, y)
        node_count += 1

    # ================= EDGE MODE =================
    elif mode == "edge":
        for nid, (nx, ny) in nodes.items():

            if (x - nx) ** 2 + (y - ny) ** 2 <= 400:

                if len(selected_nodes) == 1 and selected_nodes[0] == nid:
                    return

                selected_nodes.append(nid)

                if len(selected_nodes) == 1:
                    update_hint("Click the second node")

                if len(selected_nodes) == 2:
                    n1 = nodes[selected_nodes[0]]
                    n2 = nodes[selected_nodes[1]]

                    canvas.create_line(
                        n1[0], n1[1],
                        n2[0], n2[1],
                        fill="white",
                        width=2
                    )

                    selected_nodes.clear()
                    update_hint("Click the first node")

                break