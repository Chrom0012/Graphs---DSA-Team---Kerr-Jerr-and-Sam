"""
Part 1 of graph_interaction.py: Mode management.
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


# ── Mode management ──────────────────────────────────────────────────────────

def set_mode(new_mode):
    if state.is_running and not state.is_paused:
        return

    for action in ("vertex", "edge", "move", "delete", "edge_delete"):
        if action in state.buttons:
            try:
                state.buttons[action].config(bg="#1a1c2e", fg="white")
            except:
                pass

    state.mode = new_mode
    state.selected_vertices = []
    traversal.reset_visual_state()

    if new_mode in state.buttons:
        try:
            state.buttons[new_mode].config(bg="#00e5ff", fg="black")
        except:
            pass

    _STATUS = {
        "vertex":      ("Status: Add Vertex Mode",  "Click anywhere on the canvas to add a vertex."),
        "edge":        ("Status: Add Edge Mode",     "Click source vertex, then destination vertex."),
        "move":        ("Status: Move Mode",         "Click and drag a vertex to move it."),
        "delete":      ("Status: Delete Node Mode",  "Click inside a vertex to delete it."),
        "edge_delete": ("Status: Delete Edge Mode",  "Click near the middle of an edge to delete it."),
    }
    status, hint = _STATUS.get(new_mode, ("Status: Idle", "Select a tool from the left sidebar."))
    state.update_status(status)
    state.update_hint(hint)


def toggle_vertex():      set_mode("idle" if state.mode == "vertex"      else "vertex")
def toggle_edge():        set_mode("idle" if state.mode == "edge"        else "edge")
def toggle_move():        set_mode("idle" if state.mode == "move"        else "move")
def toggle_delete():      set_mode("idle" if state.mode == "delete"      else "delete")
def toggle_edge_delete(): set_mode("idle" if state.mode == "edge_delete" else "edge_delete")