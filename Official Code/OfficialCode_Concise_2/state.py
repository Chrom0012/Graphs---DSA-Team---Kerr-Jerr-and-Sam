import tkinter as tk

# Core Graph Properties
mode = "idle"
vertices = {}
selected_vertices = []
dragging_vertex = None
adj_list = {}
graph_type = "undirected"

# Workspace and Time Scaling Factors
waiting_for_start = None   
animation_speed = 650
is_animating = False       
zoom_scale_tracker = 1.0

# BFS/DFS Historic Step Stack Arrays
bfs_step_index = 0
bfs_order = []
bfs_parent = {}
bfs_max_depth = 0

dfs_step_index = 0
dfs_order = []
dfs_parent = {}
dfs_max_depth = 0

last_algo = None 
last_start = None
paused = False
step_requested = False

# App UI Direct Hook References
canvas = None
status_label = None
hint_label = None
progress_label = None 
process_label = None
stats_label = None
buttons = {}
set_ui_animation_state = None

def graph_is_not_empty():
    return len(vertices) > 0

def set_animation_speed(value):
    global animation_speed
    animation_speed = value

def update_hint(text):
    if hint_label:
        hint_label.config(text=text)

def update_progress(text):
    if progress_label:
        progress_label.config(state="normal")
        progress_label.delete("1.0", "end")
        progress_label.insert("end", text)
        progress_label.config(state="disabled")
        progress_label.see("end") 

def update_process(text):
    if process_label:
        process_label.config(text=text)

def update_stats_display(time_ms, visited_count, max_depth):
    if stats_label:
        stats_label.config(
            text=f"Time Elapsed: {time_ms} ms\n"
                 f"Nodes Visited: {visited_count} / {len(vertices)}\n"
                 f"Max Structure Depth: {max_depth}"
        )

def update_button_states():
    if not buttons or not set_ui_animation_state:
        return
    set_ui_animation_state(is_animating, paused)