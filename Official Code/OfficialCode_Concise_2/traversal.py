from collections import deque
import state
import animation

def resume_animation():
    if state.last_algo == "bfs":
        animate_bfs_step()
    elif state.last_algo == "dfs":
        animate_dfs_step()

def toggle_pause():
    if not state.is_animating: return
    state.paused = not state.paused
    if state.paused:
        state.update_hint("Traversal paused")
        if "pause" in state.buttons: state.buttons["pause"].config(text="▶ Resume")
    else:
        state.update_hint("Traversal resumed")
        if "pause" in state.buttons: state.buttons["pause"].config(text="⏸ Pause")
        resume_animation()
    state.update_button_states()

def step_forward():
    if not state.paused:
        state.update_hint("Pause first to step manually")
        return
    state.step_requested = True
    if state.last_algo == "bfs":
        animate_bfs_step()
    elif state.last_algo == "dfs":
        animate_dfs_step()

def step_backward():
    if not state.paused:
        state.update_hint("Pause first to step manually")
        return

    if state.last_algo == "bfs":
        if state.bfs_step_index <= 0: return
        state.bfs_step_index -= 1
        vid = state.bfs_order[state.bfs_step_index]
        state.canvas.itemconfig(state.vertices[vid]["circle"], fill="#12131f", outline="#444866", width=2)
        state.canvas.itemconfig(state.vertices[vid]["text"], fill="white")
        
        parent = state.bfs_parent[vid]
        if parent is not None:
            for neigh, edge_id in state.adj_list[parent]:
                if neigh == vid:
                    state.canvas.itemconfig(edge_id, fill="#444866", width=2)
                    break
        if state.bfs_step_index == 0:
            state.update_process("Step: 0 | Ready")
            state.update_progress("")
            state.update_stats_display(0, 0, state.bfs_max_depth)
        else:
            state.update_process(f"Step: {state.bfs_step_index} | Current: {state.bfs_order[state.bfs_step_index - 1]}")
            state.update_progress(" → ".join(map(str, state.bfs_order[:state.bfs_step_index])))
            state.update_stats_display((state.bfs_step_index - 1) * state.animation_speed, state.bfs_step_index, state.bfs_max_depth)
            
    elif state.last_algo == "dfs":
        if state.dfs_step_index <= 0: return
        state.dfs_step_index -= 1
        vid = state.dfs_order[state.dfs_step_index]
        state.canvas.itemconfig(state.vertices[vid]["circle"], fill="#12131f", outline="#444866", width=2)
        state.canvas.itemconfig(state.vertices[vid]["text"], fill="white")
        
        parent = state.dfs_parent[vid]
        if parent is not None:
            for neigh, edge_id in state.adj_list[parent]:
                if neigh == vid:
                    state.canvas.itemconfig(edge_id, fill="#444866", width=2)
                    break
        if state.dfs_step_index == 0:
            state.update_process("Step: 0 | Ready")
            state.update_progress("")
            state.update_stats_display(0, 0, state.dfs_max_depth)
        else:
            state.update_process(f"Step: {state.dfs_step_index} | Current: {state.dfs_order[state.dfs_step_index - 1]}")
            state.update_progress(" → ".join(map(str, state.dfs_order[:state.dfs_step_index])))
            state.update_stats_display((state.dfs_step_index - 1) * state.animation_speed, state.dfs_step_index, state.dfs_max_depth)

def start_bfs_mode():
    if not state.graph_is_not_empty(): return
    reset_visual_state()
    state.waiting_for_start = "bfs"
    import graph
    graph.set_mode("idle")
    state.status_label.config(text="Status: BFS Mode")

def run_bfs(start):
    state.last_algo, state.last_start = "bfs", start
    state.is_animating, state.paused = True, False
    state.update_button_states()

    visited, queue = {start}, deque([start])
    state.bfs_order, state.bfs_parent = [], {start: None}
    state.bfs_max_depth = 0

    while queue:
        state.bfs_max_depth = max(state.bfs_max_depth, len(queue))
        vertex = queue.popleft()
        state.bfs_order.append(vertex)
        for neigh, _ in state.adj_list[vertex]:
            if neigh not in visited:
                visited.add(neigh)
                queue.append(neigh)
                state.bfs_parent[neigh] = vertex

    state.bfs_step_index = 0
    animate_bfs_step()

def animate_bfs_step():
    if state.paused and not state.step_requested: return
    state.step_requested = False
    if state.bfs_step_index >= len(state.bfs_order):
        state.is_animating = False
        state.update_button_states()
        state.update_hint("BFS Complete")
        return

    vid = state.bfs_order[state.bfs_step_index]
    parent = state.bfs_parent[vid]
    
    def apply_node_arrival_visuals():
        state.update_process(f"Step: {state.bfs_step_index + 1} | Current: {vid}")
        state.update_progress(" → ".join(map(str, state.bfs_order[:state.bfs_step_index + 1])))
        state.update_stats_display(state.bfs_step_index * state.animation_speed, state.bfs_step_index + 1, state.bfs_max_depth)
        
        animation.trigger_radar_pulse(state.vertices[vid]["x"], state.vertices[vid]["y"], max_r=80, wave_color="#ffd700")
        state.canvas.itemconfig(state.vertices[vid]["circle"], fill="#ffd700", outline="#ffb300", width=4)
        state.canvas.itemconfig(state.vertices[vid]["text"], fill="black")
        
        state.bfs_step_index += 1
        if not state.paused: 
            state.canvas.after(state.animation_speed, animate_bfs_step)

    if parent is not None:
        px, py = state.vertices[parent]["x"], state.vertices[parent]["y"]
        cx, cy = state.vertices[vid]["x"], state.vertices[vid]["y"]
        for neigh, edge_id in state.adj_list[parent]:
            if neigh == vid: 
                state.canvas.itemconfig(edge_id, fill="#ffd700", width=4)
                break
        animation.fire_traveling_photon_pulse(px, py, cx, cy, "#ffd700", apply_node_arrival_visuals)
    else:
        apply_node_arrival_visuals()

def start_dfs_mode():
    if not state.graph_is_not_empty(): return
    reset_visual_state()
    state.waiting_for_start = "dfs"
    import graph
    graph.set_mode("idle")
    state.status_label.config(text="Status: DFS Mode")

def run_dfs(start):
    state.last_algo, state.last_start = "dfs", start
    state.is_animating, state.paused = True, False
    state.update_button_states()

    visited, stack = set(), [start]
    state.dfs_order, state.dfs_parent = [], {start: None}
    state.dfs_max_depth = 0

    while stack:
        state.dfs_max_depth = max(state.dfs_max_depth, len(stack))
        vertex = stack.pop()
        if vertex in visited: continue
        visited.add(vertex)
        state.dfs_order.append(vertex)
        for neigh, _ in reversed(state.adj_list[vertex]):
            if neigh not in visited: 
                state.dfs_parent[neigh] = vertex
                stack.append(neigh)

    state.dfs_step_index = 0
    animate_dfs_step()

def animate_dfs_step():
    if state.paused and not state.step_requested: return
    state.step_requested = False
    if state.dfs_step_index >= len(state.dfs_order):
        state.is_animating = False
        state.update_button_states()
        state.update_hint("DFS Complete")
        return

    vid = state.dfs_order[state.dfs_step_index]
    parent = state.dfs_parent[vid]

    def apply_node_arrival_visuals():
        state.update_process(f"Step: {state.dfs_step_index + 1} | Current: {vid}")
        state.update_progress(" → ".join(map(str, state.dfs_order[:state.dfs_step_index + 1])))
        state.update_stats_display(state.dfs_step_index * state.animation_speed, state.dfs_step_index + 1, state.dfs_max_depth)
        
        animation.trigger_radar_pulse(state.vertices[vid]["x"], state.vertices[vid]["y"], max_r=80, wave_color="#00e5ff")
        state.canvas.itemconfig(state.vertices[vid]["circle"], fill="#00e5ff", outline="#00b7ff", width=4)
        state.canvas.itemconfig(state.vertices[vid]["text"], fill="black")
        
        state.dfs_step_index += 1
        if not state.paused: 
            state.canvas.after(state.animation_speed, animate_dfs_step)

    if parent is not None:
        px, py = state.vertices[parent]["x"], state.vertices[parent]["y"]
        cx, cy = state.vertices[vid]["x"], state.vertices[vid]["y"]
        for neigh, edge_id in state.adj_list[parent]:
            if neigh == vid: 
                state.canvas.itemconfig(edge_id, fill="#00e5ff", width=4)
                break
        animation.fire_traveling_photon_pulse(px, py, cx, cy, "#00e5ff", apply_node_arrival_visuals)
    else:
        apply_node_arrival_visuals()

def restart_traversal():
    if state.last_algo is None or state.last_start is None: return
    reset_visual_state()
    state.is_animating, state.paused = True, False
    state.update_button_states()
    if "pause" in state.buttons: state.buttons["pause"].config(text="⏸ Pause")

    if state.last_algo == "bfs":
        state.bfs_step_index = 0
        animate_bfs_step()
    elif state.last_algo == "dfs":
        state.dfs_step_index = 0
        animate_dfs_step()

def reset_visual_state():
    for vid in state.vertices:
        state.canvas.itemconfig(state.vertices[vid]["circle"], fill="#12131f", outline="#444866", width=2)
        state.canvas.itemconfig(state.vertices[vid]["text"], fill="white")
    seen = set()
    for vid in state.adj_list:
        for neigh, edge_id in state.adj_list[vid]:
            if edge_id in seen: continue
            seen.add(edge_id)
            state.canvas.itemconfig(edge_id, fill="#444866", width=2)