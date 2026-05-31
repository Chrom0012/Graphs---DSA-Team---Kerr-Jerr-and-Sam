"""
Part 3 of graph_interaction.py: Mouse event handlers (move, click, add/delete vertices/edges)
"""
import tkinter as tk
from tkinter import messagebox
import state
import animation
import traversal
from graph_core import (
    get_contrast_color, edge_exists, calculate_edge_endpoints,
    redraw_graph, highlight_vertex, unhighlight_vertex,
    select_vertex, deselect_vertex
)
from vertex_dialog import ask_vertex_details   # <-- added to resolve name


# ── Mouse events ─────────────────────────────────────────────────────────────

def on_mouse_move(event):
    if state.is_running and not state.is_paused:
        return
    if not state.canvas or not state.canvas.winfo_exists():
        return
    x, y = event.x, event.y
    bound = (state.vertex_radius * state.zoom_scale_tracker) ** 2

    if state.mode == "edge_delete":
        hit_dist_sq = (22 * state.zoom_scale_tracker) ** 2
        for u in state.adj_list:
            for v, eid in state.adj_list[u]:
                try:
                    state.canvas.itemconfig(eid, fill="#555588")
                except:
                    pass
        for u in list(state.adj_list.keys()):
            for v, eid in list(state.adj_list[u]):
                try:
                    sx1, sy1, sx2, sy2 = calculate_edge_endpoints(u, v)
                    mx, my = (sx1 + sy1) / 2, (sx2 + sy2) / 2
                except:
                    ox, oy = state.vertices[u]["x"], state.vertices[u]["y"]
                    tx, ty = state.vertices[v]["x"], state.vertices[v]["y"]
                    mx, my = (ox + tx) / 2, (oy + ty) / 2
                if (x - mx) ** 2 + (y - my) ** 2 <= hit_dist_sq:
                    try:
                        state.canvas.itemconfig(eid, fill="#ff3366")
                    except:
                        pass
                    break

    hovered = None
    for vid, data in state.vertices.items():
        if (x - data["x"]) ** 2 + (y - data["y"]) ** 2 <= bound:
            hovered = vid
            break
    for vid in state.vertices:
        if vid not in state.selected_vertices:
            unhighlight_vertex(vid)
    if hovered and hovered not in state.selected_vertices:
        highlight_vertex(hovered)


def on_canvas_click(event):
    if state.is_running and not state.is_paused:
        state.update_hint("❌ Animation running – cannot edit graph.")
        return
    if not state.canvas or not state.canvas.winfo_exists():
        return
    x, y = event.x, event.y
    r_vis = state.vertex_radius * state.zoom_scale_tracker
    hit_bound = r_vis ** 2

    if state.mode == "move":
        for vid, data in state.vertices.items():
            if (x - data["x"]) ** 2 + (y - data["y"]) ** 2 <= hit_bound:
                state.dragging_vertex = vid
                return

    if state.mode == "delete":
        _handle_delete_vertex(x, y, hit_bound)
        return

    if state.mode == "edge_delete":
        _handle_delete_edge(x, y)
        return

    if state.mode in ("pick_bfs_root", "pick_dfs_root"):
        _handle_pick_root(x, y, hit_bound)
        return

    if state.mode == "vertex":
        _handle_add_vertex(x, y, r_vis)
        return

    if state.mode == "edge":
        _handle_add_edge(x, y, hit_bound, r_vis)


def _handle_delete_vertex(x, y, hit_bound):
    for vid, data in list(state.vertices.items()):
        if (x - data["x"]) ** 2 + (y - data["y"]) ** 2 <= hit_bound:
            if vid in state.selected_vertices:
                state.selected_vertices.remove(vid)
            for v in list(state.adj_list.keys()):
                new_edges = []
                for neigh, eid in state.adj_list[v]:
                    if neigh == vid or v == vid:
                        try:
                            state.canvas.delete(eid)
                        except:
                            pass
                    else:
                        new_edges.append((neigh, eid))
                state.adj_list[v] = new_edges
            try:
                state.canvas.delete(state.vertices[vid]["circle"])
                state.canvas.delete(state.vertices[vid]["text"])
            except:
                pass
            del state.vertices[vid]
            del state.adj_list[vid]
            state.vertex_data_payloads.pop(vid, None)
            state.update_adjacency_list_ui()
            return


def _handle_delete_edge(x, y):
    hit_dist_sq = (22 * state.zoom_scale_tracker) ** 2
    target = None
    for u in list(state.adj_list.keys()):
        for v, eid in list(state.adj_list[u]):
            try:
                sx1, sy1, sx2, sy2 = calculate_edge_endpoints(u, v)
                mx, my = (sx1 + sx2) / 2, (sy1 + sy2) / 2
            except:
                ox, oy = state.vertices[u]["x"], state.vertices[u]["y"]
                tx, ty = state.vertices[v]["x"], state.vertices[v]["y"]
                mx, my = (ox + tx) / 2, (oy + ty) / 2
            if (x - mx) ** 2 + (y - my) ** 2 <= hit_dist_sq:
                target = (u, v, eid)
                break
        if target:
            break
    if target:
        u, v, eid = target
        try:
            state.canvas.delete(eid)
        except:
            pass
        state.adj_list[u] = [i for i in state.adj_list[u] if i[0] != v and i[1] != eid]
        if state.graph_type == "undirected" and v in state.adj_list:
            state.adj_list[v] = [i for i in state.adj_list[v] if i[0] != u and i[1] != eid]
        state.update_hint("✂️ Edge deleted.")
        state.update_adjacency_list_ui()
        redraw_graph()


def _handle_pick_root(x, y, hit_bound):
    for vid, data in state.vertices.items():
        if (x - data["x"]) ** 2 + (y - data["y"]) ** 2 <= hit_bound:
            if state.mode == "pick_bfs_root":
                traversal.run_bfs(vid)
            else:
                traversal.run_dfs(vid)
            return
    state.update_hint("Click on a vertex to start the search.")


def _handle_add_vertex(x, y, r_vis):
    """Auto-name or prompt for custom ID, then place vertex."""
    def alpha_id(n):
        res = ""
        while n >= 0:
            res = chr(n % 26 + 65) + res; n = n // 26 - 1
        return res

    if state.vertex_naming_mode == "integer":
        candidate = 1
        while str(candidate) in state.vertices:
            candidate += 1
        vid, custom = str(candidate), ""
    elif state.vertex_naming_mode == "letter":
        idx = 0
        while alpha_id(idx) in state.vertices:
            idx += 1
        vid, custom = alpha_id(idx), ""
    else:
        vid, custom = ask_vertex_details(state.canvas.winfo_toplevel())
        if vid is None:
            return

    if vid in state.vertices:
        messagebox.showwarning("Duplicate Identity", f"Vertex '{vid}' already exists.")
        return

    color = state.vertex_fill_color
    label_color = get_contrast_color(color)
    font_sz = max(6, int(10 * state.zoom_scale_tracker))
    circle = state.canvas.create_oval(
        x - r_vis, y - r_vis, x + r_vis, y + r_vis,
        fill=color, outline="#333355",
        width=max(1, int(2 * state.zoom_scale_tracker))
    )
    display = str(vid) + (f"\n[{custom}]" if custom else "")
    text = state.canvas.create_text(
        x, y, text=display, fill=label_color,
        font=("Consolas", max(5, font_sz - 1), "bold"),
        anchor="center", justify="center"
    )
    state.vertices[vid] = {"x": x, "y": y, "circle": circle, "text": text, "color": color}
    state.vertex_data_payloads[vid] = custom
    state.adj_list[vid] = []
    animation.animate_vertex_bounce(vid, x, y)
    state.update_adjacency_list_ui()


def _handle_add_edge(x, y, hit_bound, r_vis):
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
                if a == b:
                    state.update_hint("❌ Self-loops are not allowed.")
                    for v in state.selected_vertices: deselect_vertex(v)
                    state.selected_vertices.clear()
                    return
                if edge_exists(a, b):
                    state.update_hint("❌ Edge already exists.")
                    for v in state.selected_vertices: deselect_vertex(v)
                    state.selected_vertices.clear()
                    return
                sx1, sy1, sx2, sy2 = calculate_edge_endpoints(a, b)
                lw = max(1, int(state.edge_width * state.zoom_scale_tracker))
                arrow_sz = (
                    max(5, int(11 * state.zoom_scale_tracker)),
                    max(5, int(13 * state.zoom_scale_tracker)),
                    max(2, int(5 * state.zoom_scale_tracker))
                )
                edge = state.canvas.create_line(
                    sx1, sy1, sx2, sy2,
                    fill="#555588", width=lw,
                    arrow="last" if state.graph_type == "directed" else None,
                    arrowshape=arrow_sz
                )
                state.canvas.tag_lower(edge)
                animation.animate_edge_growth(edge, sx1, sy1, sx2, sy2)
                state.adj_list[a].append((b, edge))
                if state.graph_type == "undirected":
                    state.adj_list[b].append((a, edge))
                for v in state.selected_vertices: deselect_vertex(v)
                state.selected_vertices.clear()
                state.update_hint("🔗 Edge added.")
                state.update_adjacency_list_ui()
            break