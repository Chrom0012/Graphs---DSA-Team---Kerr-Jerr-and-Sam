"""
ui_helpers.py – public API shim.
Real logic split into ui_theme.py and ui_controls.py.
"""
from ui_theme import (
    apply_hover_style,
    apply_algo_theme,
    open_color_picker,
    open_canvas_color_picker,
    apply_canvas_preset,
    safe_zoom_in,
    safe_zoom_out,
    show_search_options_popup,
    trigger_bfs_mode,
    trigger_dfs_mode,
    toggle_left_drawer,
    auto_open_right_drawer,
    auto_close_left_drawer,
    auto_open_left_drawer,
    set_ui_animation_state,
    filtered_canvas_click,
    filtered_mouse_move,
    filtered_canvas_drag,
    filtered_canvas_release,
)

from ui_controls import (
    update_size_mode_buttons,
    switch_to_radius,
    switch_to_diameter,
    on_slider_change,
    show_size_preview_popup,
    apply_vertex_size,
    on_edge_width_slider,
    apply_edge_width,
    push_target_assignment,
    apply_speed,
)
