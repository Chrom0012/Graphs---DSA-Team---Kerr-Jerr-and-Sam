"""
Part 4 of graph_interaction.py: Drag handlers and graph reset.
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
from mode_management import set_mode   # <-- added to resolve name


def on_canvas_drag(event):
    if state.is_running or state.mode != "move" or state.dragging_vertex is None:
        return
    if not state.canvas or not state.canvas.winfo_exists():
        return
    vid = state.dragging_vertex
    if vid not in state.vertices:
        state.dragging_vertex = None
        return
    x, y = event.x, event.y
    state.vertices[vid]["x"], state.vertices[vid]["y"] = x, y
    r = state.vertex_radius * state.zoom_scale_tracker
    try:
        state.canvas.coords(state.vertices[vid]["circle"], x - r, y - r, x + r, y + r)
        state.canvas.coords(state.vertices[vid]["text"], x, y)
    except:
        pass
    for u in state.adj_list:
        for v, eid in state.adj_list[u]:
            if u == vid or v == vid:
                try:
                    x1, y1, x2, y2 = calculate_edge_endpoints(u, v)
                    state.canvas.coords(eid, x1, y1, x2, y2)
                except:
                    pass


def on_canvas_release(event):
    state.dragging_vertex = None


# ── Graph reset ──────────────────────────────────────────────────────────────

def reset_graph():
    traversal.clear_any_active_timer()
    traversal.reset_visual_state()
    if state.canvas and state.canvas.winfo_exists():
        try:
            state.canvas.delete("all")
        except:
            pass
    state.vertices.clear()
    state.vertex_data_payloads.clear()
    state.adj_list.clear()
    state.selected_vertices.clear()
    state.zoom_scale_tracker = 1.0
    state.traversal_history.clear()
    state.current_step_index = 0
    state.target_vertex = None
    state.next_auto_index = 0
    state._traversal_start_time = None
    state.update_stats_display(0, 0, 0)
    state.is_running = False
    state.is_paused = False
    state.update_status("Status: Idle")
    state.update_hint("Select a tool to begin.")
    state.update_adjacency_list_ui()
    state.set_ui_animation_state(False)
    set_mode("idle")