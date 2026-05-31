import random
import math
import state
import graph
import animation

def _clear_and_prepare():
    graph.reset_graph()
    state.mode = "vertex"
    state.zoom_scale_tracker = 1.0
    if state.canvas and state.canvas.winfo_exists():
        try:
            state.canvas.xview_moveto(0.5)
            state.canvas.yview_moveto(0.5)
        except:
            pass

def _get_canvas_center():
    if not state.canvas or not state.canvas.winfo_exists():
        return 400, 300
    w = state.canvas.winfo_width()
    h = state.canvas.winfo_height()
    if w < 100 or h < 100:
        return 400, 300
    return state.canvas.canvasx(w // 2), state.canvas.canvasy(h // 2)

def _create_vertex(vid, x, y, custom_data=""):
    r = state.vertex_radius * state.zoom_scale_tracker
    color = state.vertex_fill_color
    label_color = graph.get_contrast_color(color)
    font_sz = max(6, int(10 * state.zoom_scale_tracker))
    circle = state.canvas.create_oval(
        x - r, y - r, x + r, y + r,
        fill=color, outline="#333355",
        width=max(1, int(2 * state.zoom_scale_tracker))
    )
    display = str(vid)
    if custom_data:
        display += f"\n[{custom_data}]"
    text = state.canvas.create_text(
        x, y, text=display,
        fill=label_color,
        font=("Consolas", max(5, font_sz - 1), "bold"),
        anchor="center", justify="center"
    )
    state.vertices[vid] = {"x": x, "y": y, "circle": circle, "text": text, "color": color}
    state.vertex_data_payloads[vid] = custom_data
    state.adj_list[vid] = []
    animation.animate_vertex_bounce(vid, x, y)

def _create_edge(u, v):
    from graph_core import calculate_edge_endpoints
    x1, y1, x2, y2 = calculate_edge_endpoints(u, v)
    lw = max(1, int(state.edge_width * state.zoom_scale_tracker))
    arrow_sz = (
        max(5, int(11 * state.zoom_scale_tracker)),
        max(5, int(13 * state.zoom_scale_tracker)),
        max(2, int(5 * state.zoom_scale_tracker))
    )
    edge = state.canvas.create_line(
        x1, y1, x2, y2,
        fill="#555588", width=lw,
        arrow="last" if state.graph_type == "directed" else None,
        arrowshape=arrow_sz
    )
    state.canvas.tag_lower(edge)
    state.adj_list[u].append((v, edge))
    if state.graph_type == "undirected":
        state.adj_list[v].append((u, edge))
    animation.animate_edge_growth(edge, x1, y1, x2, y2)

def simple_undirected():
    _clear_and_prepare()
    graph.set_graph_type("undirected")
    if not state.canvas or not state.canvas.winfo_exists():
        return
    cx, cy = _get_canvas_center()
    radius = 150
    positions = [(cx + radius * math.cos(math.radians(a)),
                  cy + radius * math.sin(math.radians(a))) for a in (90, 210, 330)]
    for i, (x, y) in enumerate(positions):
        _create_vertex(str(i + 1), x, y)
    _create_edge("1", "2")
    _create_edge("2", "3")
    _create_edge("3", "1")
    state.update_adjacency_list_ui()
    graph.set_mode("idle")
    graph.redraw_graph()
    state.update_hint("Loaded undirected triangle example (centered).")

def simple_directed():
    _clear_and_prepare()
    graph.set_graph_type("directed")
    if not state.canvas or not state.canvas.winfo_exists():
        return
    cx, cy = _get_canvas_center()
    _create_vertex("A", cx - 120, cy)
    _create_vertex("B", cx + 120, cy)
    _create_edge("A", "B")
    _create_edge("B", "A")
    graph.redraw_graph()
    state.update_adjacency_list_ui()
    graph.set_mode("idle")
    state.update_hint("Loaded directed bidirectional example.")

def random_graph(num_vertices, num_edges, directed=False):
    if num_vertices < 1 or num_edges < 0:
        state.update_hint("Invalid parameters.")
        return
    max_possible = num_vertices * (num_vertices - 1)
    if not directed:
        max_possible //= 2
    if num_edges > max_possible:
        state.update_hint(f"Too many edges! Max is {max_possible}.")
        return
    _clear_and_prepare()
    graph.set_graph_type("directed" if directed else "undirected")
    if not state.canvas or not state.canvas.winfo_exists():
        return
    cx, cy = _get_canvas_center()
    w = state.canvas.winfo_width()
    h = state.canvas.winfo_height()
    if w < 100 or h < 100:
        w, h = 800, 600
    radius = min(w, h) * 0.35
    angle_step = 2 * math.pi / num_vertices
    ids = []
    for i in range(num_vertices):
        angle = i * angle_step
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        vid = str(i + 1)
        _create_vertex(vid, x, y)
        ids.append(vid)
    possible = []
    for i in range(num_vertices):
        for j in range(num_vertices):
            if i == j:
                continue
            if not directed and i > j:
                continue
            possible.append((ids[i], ids[j]))
    random.shuffle(possible)
    for u, v in possible[:num_edges]:
        _create_edge(u, v)
    if directed:
        graph.redraw_graph()
    state.update_adjacency_list_ui()
    graph.set_mode("idle")
    graph.redraw_graph()
    state.update_hint(
        f"Generated random {state.graph_type} graph "
        f"with {num_vertices} vertices and {num_edges} edges."
    )
