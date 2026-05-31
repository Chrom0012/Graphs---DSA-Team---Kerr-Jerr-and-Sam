"""
graph_interaction.py - Original module facade
This file imports and re‑exports all public functions from the split files,
so that existing code that does
    from graph_interaction import set_mode, reset_graph, on_canvas_click, ...
continues to work unchanged.
"""

from mode_management import (
    set_mode,
    toggle_vertex,
    toggle_edge,
    toggle_move,
    toggle_delete,
    toggle_edge_delete,
)
from vertex_dialog import ask_vertex_details
from graph_handlers import (
    on_mouse_move,
    on_canvas_click,
)
from graph_drag_reset import (
    on_canvas_drag,
    on_canvas_release,
    reset_graph,
)

__all__ = [
    "set_mode",
    "toggle_vertex",
    "toggle_edge",
    "toggle_move",
    "toggle_delete",
    "toggle_edge_delete",
    "ask_vertex_details",
    "on_mouse_move",
    "on_canvas_click",
    "on_canvas_drag",
    "on_canvas_release",
    "reset_graph",
]