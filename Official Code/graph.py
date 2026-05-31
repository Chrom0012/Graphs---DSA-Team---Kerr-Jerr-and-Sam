"""
graph.py – public API shim.
All real logic lives in graph_core.py and graph_interaction.py.
Import this module everywhere as before.
"""
from graph_core import (
    get_contrast_color,
    edge_exists,
    calculate_edge_endpoints,
    highlight_vertex,
    unhighlight_vertex,
    select_vertex,
    deselect_vertex,
    redraw_graph,
    set_graph_type,
    execute_ui_zoom,
    start_canvas_pan,
    drag_canvas_pan,
    handle_mouse_wheel_zoom,
)

from graph_interaction import (
    set_mode,
    toggle_vertex,
    toggle_edge,
    toggle_move,
    toggle_delete,
    toggle_edge_delete,
    ask_vertex_details,
    on_mouse_move,
    on_canvas_click,
    on_canvas_drag,
    on_canvas_release,
    reset_graph,
)
