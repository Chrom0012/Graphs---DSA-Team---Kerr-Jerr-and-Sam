import tkinter as tk

mode = "idle"
vertices = {}
selected_vertices = []
dragging_vertex = None
adj_list = {}
graph_type = "undirected"

vertex_data_payloads = {}

after_id = None
animation_timer_id = None
animation_speed = 650
is_animating = False
zoom_scale_tracker = 1.0

target_vertex = None

traversal_history = []
current_step_index = 0
is_running = False
is_paused = False
_traversal_start_time = None

algo_color = "#00e5ff"

vertex_fill_color = "#1e3a5f"
vertex_radius = 22

canvas_bg_color = "#ffffff"

edge_width = 2

vertex_naming_mode = "integer"
next_auto_index = 0

canvas = None
status_label = None
hint_label = None
progress_label = None
process_label = None
stats_label = None
adj_list_display = None
frontier_display = None
buttons = {}
_status_label = None
_app_title_lbl = None
_play_search_btn = None
_stats_title = None
_frontier_box = None
_progress_box = None

_left_sidebar_canvas = None
_left_handle_btn = None
_is_left_open = None

_right_sidebar_panel = None
_right_sidebar_console = None
_right_handle_btn = None
_is_right_open = None

_set_ui_animation_state_callback = None

def set_ui_animation_state(is_running, is_paused=False):
    if _set_ui_animation_state_callback:
        _set_ui_animation_state_callback(is_running, is_paused)

def register_ui_animation_callback(callback):
    global _set_ui_animation_state_callback
    _set_ui_animation_state_callback = callback

def graph_is_not_empty():
    return len(vertices) > 0

def set_animation_speed(value):
    global animation_speed
    animation_speed = max(50, value)

def update_status(text):
    if status_label and status_label.winfo_exists():
        try:
            status_label.config(text=text)
        except Exception:
            pass

def update_hint(text):
    if hint_label and hint_label.winfo_exists():
        try:
            hint_label.config(text=text)
        except Exception:
            pass

def update_progress(text):
    if progress_label and progress_label.winfo_exists():
        try:
            progress_label.config(state="normal")
            progress_label.delete("1.0", "end")
            progress_label.insert("end", text)
            progress_label.config(state="disabled")
            progress_label.see("end")
        except Exception:
            pass

def update_process(text):
    if process_label and process_label.winfo_exists():
        try:
            process_label.config(text=text)
        except Exception:
            pass

def update_stats_display(time_ms, visited_count, step_index):
    if stats_label and stats_label.winfo_exists():
        try:
            stats_label.config(
                text=(
                    f"⏱ Time Elapsed: {time_ms} ms\n"
                    f"⬢ Nodes Visited: {visited_count} / {len(vertices)}\n"
                    f"🪵 Step Counter: #{step_index}"
                )
            )
        except Exception:
            pass

def update_live_frontier_ui(items_list, structure_type="QUEUE"):
    if frontier_display and frontier_display.winfo_exists():
        try:
            frontier_display.config(state="normal")
            frontier_display.delete("1.0", "end")
            if not items_list:
                frontier_display.insert("end", "[ EMPTY ]")
            else:
                if structure_type == "QUEUE":
                    frontier_display.insert(
                        "end",
                        "OUT ← [ " + " | ".join(map(str, items_list)) + " ] ← IN"
                    )
                else:
                    frontier_display.insert(
                        "end",
                        "TOP ↕ [ " + " ➔ ".join(map(str, reversed(items_list))) + " ]"
                    )
            frontier_display.config(state="disabled")
        except Exception:
            pass

def update_adjacency_list_ui(highlight=None):
    if adj_list_display and adj_list_display.winfo_exists():
        try:
            adj_list_display.config(state="normal")
            adj_list_display.delete("1.0", "end")
            highlight_index = None
            if not adj_list:
                adj_list_display.insert("end", "Empty Graph Representation")
            else:
                current_line = 1
                for node, edges in sorted(adj_list.items(), key=lambda x: str(x[0])):
                    neighbors = [str(dest) for dest, _ in edges]
                    payload = vertex_data_payloads.get(node, "")
                    data_str = f" ({payload})" if payload else ""
                    line = f" Vertex {node}{data_str} ➔ [ {', '.join(neighbors)} ]\n"
                    if highlight is not None and str(node) == str(highlight):
                        adj_list_display.insert("end", line, ("highlight",))
                        highlight_index = f"{current_line}.0"
                    else:
                        adj_list_display.insert("end", line)
                    current_line += 1
            adj_list_display.tag_config("highlight", foreground="#ffd700", background="#1e2a3a")
            if highlight_index:
                adj_list_display.see(highlight_index)
            adj_list_display.config(state="disabled")
        except Exception:
            pass

def update_button_states():
    set_ui_animation_state(is_running, is_paused)
