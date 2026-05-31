"""
graph_core.py
Geometry helpers, canvas drawing, and graph-type management.
"""
import math
import tkinter as tk
import state
import animation


# ── Geometry ────────────────────────────────────────────────────────────────

def get_contrast_color(hex_color):
    try:
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return "#000000" if luminance > 0.55 else "#ffffff"
    except:
        return "#ffffff"


def edge_exists(u, v):
    for neighbor, _ in state.adj_list.get(u, []):
        if neighbor == v:
            return True
    return False


def calculate_edge_endpoints(u, v):
    x1, y1 = state.vertices[u]["x"], state.vertices[u]["y"]
    x2, y2 = state.vertices[v]["x"], state.vertices[v]["y"]
    r = state.vertex_radius * state.zoom_scale_tracker

    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    if length == 0:
        return x1, y1, x2, y2

    ux, uy = dx / length, dy / length

    if state.graph_type == "directed" and edge_exists(v, u):
        h = min(12, state.vertex_radius * 0.5) * state.zoom_scale_tracker
        perp_x, perp_y = -uy, ux
        trim = math.sqrt(max(0, r**2 - h**2))
        return (x1 + perp_x * h + ux * trim, y1 + perp_y * h + uy * trim,
                x2 + perp_x * h - ux * trim, y2 + perp_y * h - uy * trim)
    else:
        return (x1 + ux * r, y1 + uy * r, x2 - ux * r, y2 - uy * r)


# ── Vertex visual helpers ────────────────────────────────────────────────────

def highlight_vertex(vid):
    if vid not in state.vertices or not state.canvas or not state.canvas.winfo_exists():
        return
    try:
        lw = max(1, int(3 * state.zoom_scale_tracker))
        theme = getattr(state, "algo_color", "#00e5ff")
        state.canvas.itemconfig(state.vertices[vid]["circle"], outline=theme, width=lw)
    except:
        pass


def unhighlight_vertex(vid):
    if vid not in state.vertices or not state.canvas or not state.canvas.winfo_exists():
        return
    try:
        lw = max(1, int(2 * state.zoom_scale_tracker))
        state.canvas.itemconfig(state.vertices[vid]["circle"], outline="#333355", width=lw)
    except:
        pass


def select_vertex(vid):
    if vid not in state.vertices or not state.canvas or not state.canvas.winfo_exists():
        return
    try:
        theme = getattr(state, "algo_color", "#00e5ff")
        state.canvas.itemconfig(state.vertices[vid]["circle"], fill=theme, outline=theme)
        state.canvas.itemconfig(state.vertices[vid]["text"], fill="black")
    except:
        pass


def deselect_vertex(vid):
    if vid not in state.vertices or not state.canvas or not state.canvas.winfo_exists():
        return
    try:
        stored = state.vertices[vid].get("color", state.vertex_fill_color)
        state.canvas.itemconfig(state.vertices[vid]["circle"], fill=stored, outline="#333355")
        state.canvas.itemconfig(state.vertices[vid]["text"], fill=get_contrast_color(stored))
    except:
        pass


# ── Full redraw ──────────────────────────────────────────────────────────────

def redraw_graph():
    if not state.canvas or not state.canvas.winfo_exists():
        return
    try:
        state.canvas.delete("all")
    except tk.TclError:
        return

    r = state.vertex_radius * state.zoom_scale_tracker
    font_size = max(6, int(10 * state.zoom_scale_tracker))
    line_width = max(1, int(state.edge_width * state.zoom_scale_tracker))
    arrow_sz = (
        max(5, int(11 * state.zoom_scale_tracker)),
        max(5, int(13 * state.zoom_scale_tracker)),
        max(2, int(5 * state.zoom_scale_tracker))
    )

    edges_to_draw, seen_undirected = [], set()
    for u in state.adj_list:
        for v, _ in state.adj_list[u]:
            if state.graph_type == "undirected":
                key = tuple(sorted([u, v]))
                if key in seen_undirected:
                    continue
                seen_undirected.add(key)
            edges_to_draw.append((u, v))

    edge_map = {}
    for u, v in edges_to_draw:
        sx1, sy1, sx2, sy2 = calculate_edge_endpoints(u, v)
        eid = state.canvas.create_line(
            sx1, sy1, sx2, sy2,
            fill="#555588", width=line_width, tags="edge",
            arrow="last" if state.graph_type == "directed" else None,
            arrowshape=arrow_sz
        )
        state.canvas.tag_lower(eid)
        edge_map[(u, v)] = eid

    new_adj = {u: [] for u in state.adj_list}
    for (u, v), eid in edge_map.items():
        new_adj[u].append((v, eid))
        if state.graph_type == "undirected":
            new_adj[v].append((u, eid))
    state.adj_list = new_adj

    for vid in list(state.vertices.keys()):
        x, y = state.vertices[vid]["x"], state.vertices[vid]["y"]
        stored_color = state.vertices[vid].get("color", state.vertex_fill_color)
        circle = state.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill=stored_color, outline="#333355",
            width=max(1, int(2 * state.zoom_scale_tracker))
        )
        display = str(vid)
        payload = state.vertex_data_payloads.get(vid, "")
        if payload:
            display += f"\n[{payload}]"
        text = state.canvas.create_text(
            x, y, text=display,
            fill=get_contrast_color(stored_color),
            font=("Consolas", max(5, font_size - 1), "bold"),
            anchor="center", justify="center"
        )
        state.vertices[vid]["circle"] = circle
        state.vertices[vid]["text"] = text

    # Re-apply traversal or selection highlights after full redraw
    if state.traversal_history:
        import traversal
        traversal.apply_step_state(state.current_step_index,
                                   trigger_effects=False, update_stats=False)
    else:
        for vid in state.selected_vertices:
            if vid in state.vertices:
                select_vertex(vid)


# ── Graph type & zoom ────────────────────────────────────────────────────────

def set_graph_type(gtype):
    state.graph_type = gtype
    state.update_hint(f"Graph type set to {gtype.upper()}")
    redraw_graph()


def execute_ui_zoom(factor, cx, cy):
    new_scale = state.zoom_scale_tracker * factor
    if 0.35 < new_scale < 3.0:
        state.zoom_scale_tracker = new_scale
        for vid in state.vertices:
            state.vertices[vid]["x"] = cx + (state.vertices[vid]["x"] - cx) * factor
            state.vertices[vid]["y"] = cy + (state.vertices[vid]["y"] - cy) * factor
        redraw_graph()


def start_canvas_pan(event):
    if state.canvas and state.canvas.winfo_exists():
        try:
            state.canvas.scan_mark(event.x, event.y)
        except:
            pass


def drag_canvas_pan(event):
    if state.canvas and state.canvas.winfo_exists():
        try:
            state.canvas.scan_dragto(event.x, event.y, gain=1)
        except:
            pass


def handle_mouse_wheel_zoom(event):
    if not state.canvas or not state.canvas.winfo_exists():
        return
    try:
        cx = state.canvas.canvasx(event.x)
        cy = state.canvas.canvasy(event.y)
        factor = 1.12 if event.delta > 0 else 0.88
        execute_ui_zoom(factor, cx, cy)
    except:
        pass
