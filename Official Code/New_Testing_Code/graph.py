# ================= GRAPH LOGIC =================
from collections import deque
import math

mode = "idle"
vertices = {}
selected_vertices = []
dragging_vertex = None
adj_list = {}
graph_type = "undirected"

waiting_for_start = None   
animation_speed = 650
is_animating = False       
zoom_scale_tracker = 1.0

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

canvas = None
status_label = None
hint_label = None
progress_label = None 
process_label = None
stats_label = None

paused = False
step_requested = False
buttons = {}
set_ui_animation_state = None

def graph_is_not_empty():
    return len(vertices) > 0

# ================= UI REFS =================

def set_ui_refs(c, status, hint, progress, process, stats):
    global canvas, status_label, hint_label, progress_label, process_label, stats_label
    canvas = c
    status_label = status
    hint_label = hint
    progress_label = progress
    process_label = process
    stats_label = stats

def set_button_refs(btn_dict):
    global buttons
    buttons = btn_dict
    update_button_states()

def update_button_states():
    if not buttons or not set_ui_animation_state:
        return
    set_ui_animation_state(is_animating, paused)

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

def set_animation_speed(value):
    global animation_speed
    animation_speed = value

def resume_animation():
    if last_algo == "bfs":
        animate_bfs_step()
    elif last_algo == "dfs":
        animate_dfs_step()

def set_graph_type(gtype):
    global graph_type
    graph_type = gtype
    if gtype == "directed":
        update_hint("Graph set to Directed")
    else:
        update_hint("Graph set to Undirected")

# ================= INFINITE WORKSPACE SCALING & PANNING ENGINE =================

def start_canvas_pan(event):
    canvas.scan_mark(event.x, event.y)

def drag_canvas_pan(event):
    canvas.scan_dragto(event.x, event.y, gain=1)

def handle_mouse_wheel_zoom(event):
    cx = canvas.canvasx(event.x)
    cy = canvas.canvasy(event.y)
    factor = 1.12 if event.delta > 0 else 0.88
    execute_ui_zoom(factor, cx, cy)

def execute_ui_zoom(factor, cx, cy):
    global zoom_scale_tracker
    if 0.35 < (zoom_scale_tracker * factor) < 3.0:
        zoom_scale_tracker *= factor
        canvas.scale("all", cx, cy, factor, factor)
        for vid in vertices:
            vertices[vid]["x"] = cx + (vertices[vid]["x"] - cx) * factor
            vertices[vid]["y"] = cy + (vertices[vid]["y"] - cy) * factor


# ================= HIGH FIDELITY GRAPHICAL TRANSITIONS =================

def animate_vertex_bounce(vid, cx, cy, frame=0):
    radius_sequence = [4, 11, 19, 27, 24, 21, 22]
    if frame >= len(radius_sequence) or vid not in vertices:
        return
    r = radius_sequence[frame]
    canvas.coords(vertices[vid]["circle"], cx - r, cy - r, cx + r, cy + r)
    canvas.after(20, lambda: animate_vertex_bounce(vid, cx, cy, frame + 1))

def animate_edge_growth(edge_id, sx, sy, ex, ey, frame=0, total_frames=8):
    if frame > total_frames:
        return
    pct = frame / total_frames
    cx = sx + (ex - sx) * pct
    cy = sy + (ey - sy) * pct
    canvas.coords(edge_id, sx, sy, cx, cy)
    canvas.after(20, lambda: animate_edge_growth(edge_id, sx, sy, ex, ey, frame + 1, total_frames))

def trigger_radar_pulse(cx, cy, max_r=75, current_r=22, wave_color="#ffd700"):
    if current_r >= max_r:
        return
    pulse_id = canvas.create_oval(
        cx - current_r, cy - current_r, cx + current_r, cy + current_r, outline=wave_color, width=2
    )
    canvas.tag_lower(pulse_id)
    canvas.after(45, lambda: canvas.delete(pulse_id))
    canvas.after(25, lambda: trigger_radar_pulse(cx, cy, max_r, current_r + 6, wave_color))

def fire_traveling_photon_pulse(sx, sy, ex, ey, color, completion_callback, frame=0, total_frames=12):
    if frame > total_frames:
        completion_callback()
        return
    pct = frame / total_frames
    cx = sx + (ex - sx) * pct
    cy = sy + (ey - sy) * pct
    
    dot_r = 6 * zoom_scale_tracker
    pulse_dot = canvas.create_oval(cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r, fill=color, outline="")
    
    canvas.after(20, lambda: [canvas.delete(pulse_dot), 
                             fire_traveling_photon_pulse(sx, sy, ex, ey, color, completion_callback, frame + 1, total_frames)])


# ================= PLAYBACK CONTROLLERS =================

def step_forward():
    global step_requested
    if not paused:
        update_hint("Pause first to step manually")
        return
    step_requested = True
    if last_algo == "bfs":
        animate_bfs_step()
    elif last_algo == "dfs":
        animate_dfs_step()

def step_backward():
    global bfs_step_index, dfs_step_index
    if not paused:
        update_hint("Pause first to step manually")
        return

    if last_algo == "bfs":
        if bfs_step_index <= 0: return
        bfs_step_index -= 1
        vid = bfs_order[bfs_step_index]
        canvas.itemconfig(vertices[vid]["circle"], fill="#12131f", outline="#444866", width=2)
        canvas.itemconfig(vertices[vid]["text"], fill="white")
        
        parent = bfs_parent[vid]
        if parent is not None:
            for neigh, edge_id in adj_list[parent]:
                if neigh == vid:
                    canvas.itemconfig(edge_id, fill="#444866", width=2)
                    break
        if bfs_step_index == 0:
            update_process("Step: 0 | Ready")
            update_progress("")
            update_stats_display(0, 0, bfs_max_depth)
        else:
            update_process(f"Step: {bfs_step_index} | Current: {bfs_order[bfs_step_index - 1]}")
            update_progress(" → ".join(map(str, bfs_order[:bfs_step_index])))
            update_stats_display((bfs_step_index - 1) * animation_speed, bfs_step_index, bfs_max_depth)
            
    elif last_algo == "dfs":
        if dfs_step_index <= 0: return
        dfs_step_index -= 1
        vid = dfs_order[dfs_step_index]
        canvas.itemconfig(vertices[vid]["circle"], fill="#12131f", outline="#444866", width=2)
        canvas.itemconfig(vertices[vid]["text"], fill="white")
        
        parent = dfs_parent[vid]
        if parent is not None:
            for neigh, edge_id in adj_list[parent]:
                if neigh == vid:
                    canvas.itemconfig(edge_id, fill="#444866", width=2)
                    break
        if dfs_step_index == 0:
            update_process("Step: 0 | Ready")
            update_progress("")
            update_stats_display(0, 0, dfs_max_depth)
        else:
            update_process(f"Step: {dfs_step_index} | Current: {dfs_order[dfs_step_index - 1]}")
            update_progress(" → ".join(map(str, dfs_order[:dfs_step_index])))
            update_stats_display((dfs_step_index - 1) * animation_speed, dfs_step_index, dfs_max_depth)

# ================= MODE CONTROL =================

def set_mode(new_mode):
    global mode, selected_vertices, waiting_for_start
    if is_animating and not paused:
        return
    mode = new_mode
    selected_vertices = []
    if new_mode != "idle": waiting_for_start = None
    reset_visual_state()

    if mode == "vertex":
        status_label.config(text="Status: Add Vertex Mode")
        update_hint("Click anywhere to add vertex")
    elif mode == "edge":
        status_label.config(text="Status: Add Edge Mode")
        update_hint("Click first vertex")
    elif new_mode == "move":
        status_label.config(text="Status: Move Mode")
        update_hint("Hold and drag a vertex to move it")
    elif new_mode == "delete":
        status_label.config(text="Status: Delete Mode")
        update_hint("Click a vertex to delete it")
    else:
        status_label.config(text="Status: Idle")
        update_hint("Select a mode to begin")

def toggle_vertex(): set_mode("idle" if mode == "vertex" else "vertex")
def toggle_edge(): set_mode("idle" if mode == "edge" else "edge")
def toggle_move(): set_mode("idle" if mode == "move" else "move")
def toggle_delete(): set_mode("idle" if mode == "delete" else "delete")

def toggle_pause():
    global paused
    if not is_animating: return
    paused = not paused
    if paused:
        update_hint("Traversal paused")
        if "pause" in buttons: buttons["pause"].config(text="▶ Resume")
    else:
        update_hint("Traversal resumed")
        if "pause" in buttons: buttons["pause"].config(text="⏸ Pause")
        resume_animation()
    update_button_states()

# ================= CANVAS EVENT HIT DETECTION AND WRITING =================

def get_edge_points(x1, y1, x2, y2):
    r = 22 * zoom_scale_tracker
    dx, dy = x2 - x1, y2 - y1
    dist = math.sqrt(dx*dx + dy*dy)
    if dist == 0: return x1, y1, x2, y2
    return x1 + (dx/dist)*r, y1 + (dy/dist)*r, x2 - (dx/dist)*r, y2 - (dy/dist)*r

def highlight_vertex(vid):
    canvas.itemconfig(vertices[vid]["circle"], outline="#00e5ff", width=3)

def unhighlight_vertex(vid):
    canvas.itemconfig(vertices[vid]["circle"], outline="#444866", width=2)

def select_vertex(vid):
    canvas.itemconfig(vertices[vid]["circle"], fill="#00e5ff", outline="#00e5ff")
    canvas.itemconfig(vertices[vid]["text"], fill="black")

def deselect_vertex(vid):
    canvas.itemconfig(vertices[vid]["circle"], fill="#12131f", outline="#444866")
    canvas.itemconfig(vertices[vid]["text"], fill="white")

def on_mouse_move(event):
    if is_animating and not paused: return
    x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)
    hovered = None
    hit_bound = (22 * zoom_scale_tracker) ** 2
    for vid, data in vertices.items():
        if (x - data["x"]) ** 2 + (y - data["y"]) ** 2 <= hit_bound:
            hovered = vid; break
    for vid in vertices:
        if vid not in selected_vertices: unhighlight_vertex(vid)
    if hovered is not None and hovered not in selected_vertices: highlight_vertex(hovered)

def on_canvas_click(event):
    global waiting_for_start, dragging_vertex
    if is_animating and not paused: return
    x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)
    hit_bound = (22 * zoom_scale_tracker) ** 2

    if mode == "move":
        for vid, data in vertices.items():
            if (x - data["x"]) ** 2 + (y - data["y"]) ** 2 <= hit_bound:
                dragging_vertex = vid; return
            
    if mode == "delete":
        for vid, data in list(vertices.items()):
            if (x - data["x"]) ** 2 + (y - data["y"]) ** 2 <= hit_bound:
                for v in list(adj_list.keys()):
                    new_list = []
                    for neigh, edge_id in adj_list[v]:
                        if neigh == vid or v == vid: canvas.delete(edge_id)
                        else: new_list.append((neigh, edge_id))
                    adj_list[v] = new_list
                canvas.delete(vertices[vid]["circle"])
                canvas.delete(vertices[vid]["text"])
                del vertices[vid]; del adj_list[vid]
                return

    if mode == "idle" and waiting_for_start is not None:
        for vid, data in vertices.items():
            if (x - data["x"]) ** 2 + (y - data["y"]) ** 2 <= hit_bound:
                algo = waiting_for_start; waiting_for_start = None
                if algo == "bfs": run_bfs(vid)
                elif algo == "dfs": run_dfs(vid)
                return

    if mode == "vertex":
        vid = 0
        while vid in vertices: vid += 1
        circle = canvas.create_oval(x, y, x, y, fill="#12131f", outline="#444866", width=2)
        text = canvas.create_text(x, y, text=str(vid), fill="white", font=("42dot Sans", int(11*zoom_scale_tracker), "bold"))
        vertices[vid] = {"x": x, "y": y, "circle": circle, "text": text}
        adj_list[vid] = []
        animate_vertex_bounce(vid, x, y)

    elif mode == "edge":
        for vid, data in vertices.items():
            if (x - data["x"]) ** 2 + (y - data["y"]) ** 2 <= hit_bound:
                if len(selected_vertices) == 1 and selected_vertices[0] == vid:
                    deselect_vertex(vid); selected_vertices.clear(); return
                selected_vertices.append(vid); select_vertex(vid)
                if len(selected_vertices) == 2:
                    a, b = selected_vertices
                    x1, y1, x2, y2 = get_edge_points(vertices[a]["x"], vertices[a]["y"], vertices[b]["x"], vertices[b]["y"])
                    edge = canvas.create_line(x1, y1, x1, y1, fill="#444866", width=2, tags="edge",
                                              arrow="last" if graph_type == "directed" else None, arrowshape=(11, 13, 5))
                    canvas.tag_lower(edge)
                    animate_edge_growth(edge, x1, y1, x2, y2)
                    adj_list[a].append((b, edge))
                    if graph_type == "undirected": adj_list[b].append((a, edge))
                    for v2 in selected_vertices: deselect_vertex(v2)
                    selected_vertices.clear()
                break

# ================= BFS SYSTEM OPERATIONS =================

def start_bfs_mode():
    if not graph_is_not_empty(): return
    reset_visual_state(); global waiting_for_start; waiting_for_start = "bfs"
    set_mode("idle"); status_label.config(text="Status: BFS Mode")

def run_bfs(start):
    global bfs_order, bfs_parent, bfs_step_index, last_algo, last_start, is_animating, paused, bfs_max_depth
    last_algo, last_start = "bfs", start
    is_animating, paused = True, False
    update_button_states()

    visited, queue = {start}, deque([start])
    bfs_order, bfs_parent = [], {start: None}
    bfs_max_depth = 0

    while queue:
        bfs_max_depth = max(bfs_max_depth, len(queue))
        vertex = queue.popleft()
        bfs_order.append(vertex)
        for neigh, _ in adj_list[vertex]:
            if neigh not in visited:
                visited.add(neigh); queue.append(neigh); bfs_parent[neigh] = vertex

    bfs_step_index = 0
    animate_bfs_step()

def animate_bfs_step():
    global bfs_step_index, step_requested, is_animating
    if paused and not step_requested: return
    step_requested = False
    if bfs_step_index >= len(bfs_order):
        is_animating = False; update_button_states(); update_hint("BFS Complete"); return

    vid = bfs_order[bfs_step_index]
    parent = bfs_parent[vid]
    
    def apply_node_arrival_visuals():
        global bfs_step_index
        update_process(f"Step: {bfs_step_index + 1} | Current: {vid}")
        update_progress(" → ".join(map(str, bfs_order[:bfs_step_index + 1])))
        update_stats_display(bfs_step_index * animation_speed, bfs_step_index + 1, bfs_max_depth)
        
        trigger_radar_pulse(vertices[vid]["x"], vertices[vid]["y"], max_r=80, wave_color="#ffd700")
        canvas.itemconfig(vertices[vid]["circle"], fill="#ffd700", outline="#ffb300", width=4)
        canvas.itemconfig(vertices[vid]["text"], fill="black")
        
        bfs_step_index += 1
        if not paused: 
            canvas.after(animation_speed, animate_bfs_step)

    if parent is not None:
        px, py = vertices[parent]["x"], vertices[parent]["y"]
        cx, cy = vertices[vid]["x"], vertices[vid]["y"]
        for neigh, edge_id in adj_list[parent]:
            if neigh == vid: canvas.itemconfig(edge_id, fill="#ffd700", width=4); break
        fire_traveling_photon_pulse(px, py, cx, cy, "#ffd700", apply_node_arrival_visuals)
    else:
        apply_node_arrival_visuals()

# ================= DFS SYSTEM OPERATIONS =================

def start_dfs_mode():
    if not graph_is_not_empty(): return
    reset_visual_state(); global waiting_for_start; waiting_for_start = "dfs"
    set_mode("idle"); status_label.config(text="Status: DFS Mode")

def run_dfs(start):
    global dfs_order, dfs_parent, dfs_step_index, last_algo, last_start, is_animating, paused, dfs_max_depth
    last_algo, last_start = "dfs", start
    is_animating, paused = True, False
    update_button_states()

    visited, stack = set(), [start]
    dfs_order, dfs_parent = [], {start: None}
    dfs_max_depth = 0

    while stack:
        dfs_max_depth = max(dfs_max_depth, len(stack))
        vertex = stack.pop()
        if vertex in visited: continue
        visited.add(vertex); dfs_order.append(vertex)
        for neigh, _ in reversed(adj_list[vertex]):
            if neigh not in visited: dfs_parent[neigh] = vertex; stack.append(neigh)

    dfs_step_index = 0
    animate_dfs_step()

def animate_dfs_step():
    global dfs_step_index, step_requested, is_animating
    if paused and not step_requested: return
    step_requested = False
    if dfs_step_index >= len(dfs_order):
        is_animating = False; update_button_states(); update_hint("DFS Complete"); return

    vid = dfs_order[dfs_step_index]
    parent = dfs_parent[vid]

    def apply_node_arrival_visuals():
        global dfs_step_index
        update_process(f"Step: {dfs_step_index + 1} | Current: {vid}")
        update_progress(" → ".join(map(str, dfs_order[:dfs_step_index + 1])))
        update_stats_display(dfs_step_index * animation_speed, dfs_step_index + 1, dfs_max_depth)
        
        trigger_radar_pulse(vertices[vid]["x"], vertices[vid]["y"], max_r=80, wave_color="#00e5ff")
        canvas.itemconfig(vertices[vid]["circle"], fill="#00e5ff", outline="#00b7ff", width=4)
        canvas.itemconfig(vertices[vid]["text"], fill="black")
        
        dfs_step_index += 1
        if not paused: canvas.after(animation_speed, animate_dfs_step)

    if parent is not None:
        px, py = vertices[parent]["x"], vertices[parent]["y"]
        cx, cy = vertices[vid]["x"], vertices[vid]["y"]
        for neigh, edge_id in adj_list[parent]:
            if neigh == vid: canvas.itemconfig(edge_id, fill="#00e5ff", width=4); break
        fire_traveling_photon_pulse(px, py, cx, cy, "#00e5ff", apply_node_arrival_visuals)
    else:
        apply_node_arrival_visuals()

# ================= RESETS & CLEANUPS =================

def restart_traversal():
    if last_algo is None or last_start is None: return
    reset_visual_state()
    global is_animating, paused, bfs_step_index, dfs_step_index
    is_animating, paused = True, False
    update_button_states()
    if "pause" in buttons: buttons["pause"].config(text="⏸ Pause")

    if last_algo == "bfs":
        bfs_step_index = 0; animate_bfs_step()
    elif last_algo == "dfs":
        dfs_step_index = 0; animate_dfs_step()

def reset_graph():
    global vertices, adj_list, selected_vertices, waiting_for_start, zoom_scale_tracker
    global bfs_step_index, bfs_order, bfs_parent, dfs_step_index, dfs_order, dfs_parent, is_animating, paused

    is_animating, paused = False, False
    canvas.delete("all")
    vertices.clear(); adj_list.clear(); selected_vertices.clear()
    waiting_for_start = None; zoom_scale_tracker = 1.0
    bfs_step_index = dfs_step_index = 0
    bfs_order, dfs_order = [], []
    bfs_parent, dfs_parent = {}, {}

    if "pause" in buttons: buttons["pause"].config(text="⏸ Pause")
    status_label.config(text="Status: Idle")
    update_hint("Select a mode to begin")
    update_progress(""); update_process(""); update_stats_display(0, 0, 0)
    update_button_states(); set_mode("idle")

def reset_visual_state():
    for vid in vertices:
        canvas.itemconfig(vertices[vid]["circle"], fill="#12131f", outline="#444866", width=2)
        canvas.itemconfig(vertices[vid]["text"], fill="white")
    seen = set()
    for vid in adj_list:
        for neigh, edge_id in adj_list[vid]:
            if edge_id in seen: continue
            seen.add(edge_id); canvas.itemconfig(edge_id, fill="#444866", width=2)
        
def on_canvas_drag(event):
    global dragging_vertex
    if is_animating or mode != "move" or dragging_vertex is None: return
    x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)
    vid = dragging_vertex

    vertices[vid]["x"], vertices[vid]["y"] = x, y
    r = 22 * zoom_scale_tracker
    canvas.coords(vertices[vid]["circle"], x - r, y - r, x + r, y + r)
    canvas.coords(vertices[vid]["text"], x, y)

    for v in adj_list:
        for neigh, edge_id in adj_list[v]:
            if v == vid or neigh == vid:
                x1, y1, x2, y2 = get_edge_points(vertices[v]["x"], vertices[v]["y"], vertices[neigh]["x"], vertices[neigh]["y"])
                canvas.coords(edge_id, x1, y1, x2, y2)

def on_canvas_release(event):
    global dragging_vertex; dragging_vertex = None