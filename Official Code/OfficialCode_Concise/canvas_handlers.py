# canvas_handlers.py - Canvas drawing, hover, and mode toggles
import animation as anim   # ← THIS LINE FIXES THE ERROR

mode = "idle"
vertex_count = 0
vertices = {}           # {vid: {"x":, "y":, "circle":, "text":}}
selected_vertices = []

canvas = None

def set_canvas(c):
    global canvas
    canvas = c

# ================= MODE TOGGLES =================
def toggle_vertex():
    global mode
    mode = "idle" if mode == "vertex" else "vertex"

def toggle_edge():
    global mode
    mode = "idle" if mode == "edge" else "edge"

def toggle_delete():
    global mode
    mode = "idle" if mode == "delete" else "delete"
    if mode == "delete":
        anim.update_console("Delete Mode: Click vertex or edge to delete")
    else:
        anim.update_console("Click first vertex")

# ================= DRAWING FUNCTIONS =================
def add_vertex(x, y):
    global vertex_count
    r = 20
    circle = canvas.create_oval(x-r, y-r, x+r, y+r, fill="white", outline="white", width=2)
    text = canvas.create_text(x, y, text=str(vertex_count), fill="black")
    vertices[vertex_count] = {"x": x, "y": y, "circle": circle, "text": text}
    vertex_count += 1
    return vertex_count - 1

def add_edge(v1, v2):
    n1 = vertices[v1]
    n2 = vertices[v2]
    edge = canvas.create_line(n1["x"], n1["y"], n2["x"], n2["y"],
                              fill="#6f6f6f", width=3, tags="edge")
    canvas.tag_lower(edge)
    return edge

# ================= VISUAL HELPERS =================
def highlight_vertex(vid):
    canvas.itemconfig(vertices[vid]["circle"], outline="lime", width=4)

def unhighlight_vertex(vid):
    canvas.itemconfig(vertices[vid]["circle"], outline="white", width=2)

def select_vertex(vid):
    canvas.itemconfig(vertices[vid]["circle"], fill="lime", outline="lime")

def deselect_vertex(vid):
    canvas.itemconfig(vertices[vid]["circle"], fill="white", outline="white")

# ================= HOVER =================
def on_mouse_move(event):
    if mode != "edge":
        return
    x, y = event.x, event.y
    hovered = None
    for vid, data in vertices.items():
        vx, vy = data["x"], data["y"]
        if (x - vx) ** 2 + (y - vy) ** 2 <= 400:
            hovered = vid
            break
    for vid in vertices:
        if vid not in selected_vertices:
            unhighlight_vertex(vid)
    if hovered is not None and hovered not in selected_vertices:
        highlight_vertex(hovered)