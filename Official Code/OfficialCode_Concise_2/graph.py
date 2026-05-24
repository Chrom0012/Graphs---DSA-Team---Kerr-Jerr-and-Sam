import math
import state
import animation
import traversal

def get_edge_points(x1, y1, x2, y2):
    r = 22 * state.zoom_scale_tracker
    dx, dy = x2 - x1, y2 - y1
    dist = math.sqrt(dx*dx + dy*dy)
    if dist == 0: return x1, y1, x2, y2
    return x1 + (dx/dist)*r, y1 + (dy/dist)*r, x2 - (dx/dist)*r, y2 - (dy/dist)*r

def highlight_vertex(vid):
    state.canvas.itemconfig(state.vertices[vid]["circle"], outline="#00e5ff", width=3)

def unhighlight_vertex(vid):
    state.canvas.itemconfig(state.vertices[vid]["circle"], outline="#444866", width=2)

def select_vertex(vid):
    state.canvas.itemconfig(state.vertices[vid]["circle"], fill="#00e5ff", outline="#00e5ff")
    state.canvas.itemconfig(state.vertices[vid]["text"], fill="black")

def deselect_vertex(vid):
    state.canvas.itemconfig(state.vertices[vid]["circle"], fill="#12131f", outline="#444866")
    state.canvas.itemconfig(state.vertices[vid]["text"], fill="white")

def set_mode(new_mode):
    if state.is_animating and not state.paused:
        return
    state.mode = new_mode
    state.selected_vertices = []
    if new_mode != "idle": state.waiting_for_start = None
    traversal.reset_visual_state()

    if state.mode == "vertex":
        state.status_label.config(text="Status: Add Vertex Mode")
        state.update_hint("Click anywhere to add vertex")
    elif state.mode == "edge":
        state.status_label.config(text="Status: Add Edge Mode")
        state.update_hint("Click first vertex")
    elif new_mode == "move":
        state.status_label.config(text="Status: Move Mode")
        state.update_hint("Hold and drag a vertex to move it")
    elif new_mode == "delete":
        state.status_label.config(text="Status: Delete Mode")
        state.update_hint("Click a vertex to delete it")
    else:
        state.status_label.config(text="Status: Idle")
        state.update_hint("Select a mode to begin")

def toggle_vertex(): set_mode("idle" if state.mode == "vertex" else "vertex")
def toggle_edge(): set_mode("idle" if state.mode == "edge" else "edge")
def toggle_move(): set_mode("idle" if state.mode == "move" else "move")
def toggle_delete(): set_mode("idle" if state.mode == "delete" else "delete")

def set_graph_type(gtype):
    state.graph_type = gtype
    if gtype == "directed":
        state.update_hint("Graph set to Directed")
    else:
        state.update_hint("Graph set to Undirected")

# Infinite Workspace Transformation Coordinates
def start_canvas_pan(event):
    state.canvas.scan_mark(event.x, event.y)

def drag_canvas_pan(event):
    state.canvas.scan_dragto(event.x, event.y, gain=1)

def handle_mouse_wheel_zoom(event):
    cx = state.canvas.canvasx(event.x)
    cy = state.canvas.canvasy(event.y)
    factor = 1.12 if event.delta > 0 else 0.88
    execute_ui_zoom(factor, cx, cy)

def execute_ui_zoom(factor, cx, cy):
    if 0.35 < (state.zoom_scale_tracker * factor) < 3.0:
        state.zoom_scale_tracker *= factor
        state.canvas.scale("all", cx, cy, factor, factor)
        for vid in state.vertices:
            state.vertices[vid]["x"] = cx + (state.vertices[vid]["x"] - cx) * factor
            state.vertices[vid]["y"] = cy + (state.vertices[vid]["y"] - cy) * factor

def on_mouse_move(event):
    if state.is_animating and not state.paused: return
    x, y = state.canvas.canvasx(event.x), state.canvas.canvasy(event.y)
    hovered = None
    hit_bound = (22 * state.zoom_scale_tracker) ** 2
    for vid, data in state.vertices.items():
        if (x - data["x"]) ** 2 + (y - data["y"]) ** 2 <= hit_bound:
            hovered = vid
            break
    for vid in state.vertices:
        if vid not in state.selected_vertices: unhighlight_vertex(vid)
    if hovered is not None and hovered not in state.selected_vertices: highlight_vertex(hovered)

def on_canvas_click(event):
    if state.is_animating and not state.paused: return
    x, y = state.canvas.canvasx(event.x), state.canvas.canvasy(event.y)
    hit_bound = (22 * state.zoom_scale_tracker) ** 2

    if state.mode == "move":
        for vid, data in state.vertices.items():
            if (x - data["x"]) ** 2 + (y - data["y"]) ** 2 <= hit_bound:
                state.dragging_vertex = vid
                return
            
    if state.mode == "delete":
        for vid, data in list(state.vertices.items()):
            if (x - data["x"]) ** 2 + (y - data["y"]) ** 2 <= hit_bound:
                for v in list(state.adj_list.keys()):
                    new_list = []
                    for neigh, edge_id in state.adj_list[v]:
                        if neigh == vid or v == vid: state.canvas.delete(edge_id)
                        else: new_list.append((neigh, edge_id))
                    state.adj_list[v] = new_list
                state.canvas.delete(state.vertices[vid]["circle"])
                state.canvas.delete(state.vertices[vid]["text"])
                del state.vertices[vid]
                del state.adj_list[vid]
                return

    if state.mode == "idle" and state.waiting_for_start is not None:
        for vid, data in state.vertices.items():
            if (x - data["x"]) ** 2 + (y - data["y"]) ** 2 <= hit_bound:
                algo = state.waiting_for_start
                state.waiting_for_start = None
                if algo == "bfs": traversal.run_bfs(vid)
                elif algo == "dfs": traversal.run_dfs(vid)
                return

    if state.mode == "vertex":
        vid = 0
        while vid in state.vertices: vid += 1
        circle = state.canvas.create_oval(x, y, x, y, fill="#12131f", outline="#444866", width=2)
        text = state.canvas.create_text(x, y, text=str(vid), fill="white", font=("42dot Sans", int(11*state.zoom_scale_tracker), "bold"))
        state.vertices[vid] = {"x": x, "y": y, "circle": circle, "text": text}
        state.adj_list[vid] = []
        animation.animate_vertex_bounce(vid, x, y)

    elif state.mode == "edge":
        for vid, data in state.vertices.items():
            if (x - data["x"]) ** 2 + (y - data["y"]) ** 2 <= hit_bound:
                if len(state.selected_vertices) == 1 and state.selected_vertices[0] == vid:
                    deselect_vertex(vid)
                    state.selected_vertices.clear()
                    return
                state.selected_vertices.append(vid)
                select_vertex(vid)
                if len(state.selected_vertices) == 2:
                    a, b = state.selected_vertices
                    x1, y1, x2, y2 = get_edge_points(state.vertices[a]["x"], state.vertices[a]["y"], state.vertices[b]["x"], state.vertices[b]["y"])
                    edge = state.canvas.create_line(x1, y1, x1, y1, fill="#444866", width=2, tags="edge",
                                              arrow="last" if state.graph_type == "directed" else None, arrowshape=(11, 13, 5))
                    state.canvas.tag_lower(edge)
                    animation.animate_edge_growth(edge, x1, y1, x2, y2)
                    state.adj_list[a].append((b, edge))
                    if state.graph_type == "undirected": state.adj_list[b].append((a, edge))
                    for v2 in state.selected_vertices: deselect_vertex(v2)
                    state.selected_vertices.clear()
                break

def on_canvas_drag(event):
    if state.is_animating or state.mode != "move" or state.dragging_vertex is None: return
    x, y = state.canvas.canvasx(event.x), state.canvas.canvasy(event.y)
    vid = state.dragging_vertex

    state.vertices[vid]["x"], state.vertices[vid]["y"] = x, y
    r = 22 * state.zoom_scale_tracker
    state.canvas.coords(state.vertices[vid]["circle"], x - r, y - r, x + r, y + r)
    state.canvas.coords(state.vertices[vid]["text"], x, y)

    for v in state.adj_list:
        for neigh, edge_id in state.adj_list[v]:
            if v == vid or neigh == vid:
                x1, y1, x2, y2 = get_edge_points(state.vertices[v]["x"], state.vertices[v]["y"], state.vertices[neigh]["x"], state.vertices[neigh]["y"])
                state.canvas.coords(edge_id, x1, y1, x2, y2)

def on_canvas_release(event):
    state.dragging_vertex = None

def reset_graph():
    state.is_animating, state.paused = False, False
    state.canvas.delete("all")
    state.vertices.clear()
    state.adj_list.clear()
    state.selected_vertices.clear()
    state.waiting_for_start = None
    state.zoom_scale_tracker = 1.0
    state.bfs_step_index = state.dfs_step_index = 0
    state.bfs_order, state.dfs_order = [], []
    state.bfs_parent, state.dfs_parent = {}, {}

    if "pause" in state.buttons: state.buttons["pause"].config(text="⏸ Pause")
    state.status_label.config(text="Status: Idle")
    state.update_hint("Select a mode to begin")
    state.update_progress("")
    state.update_process("")
    state.update_stats_display(0, 0, 0)
    state.update_button_states()
    set_mode("idle")