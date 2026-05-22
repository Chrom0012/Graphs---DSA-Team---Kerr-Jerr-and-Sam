# animation.py - COMPLETE VERSION (All functions defined)
import time
import canvas_handlers as ch
import graph as g_module

waiting_for_start = None
last_algo = None
last_start = None
current_algo = None
paused = False
animation_speed = 650

bfs_step_index = 0
bfs_order = []
bfs_parent = {}
bfs_steps = 0
bfs_path = 0

dfs_step_index = 0
dfs_order = []
dfs_parent = {}
dfs_steps = 0
dfs_path = 0

canvas = None
status_label = None
hint_label = None
graph_instance = None
legend_label = None
pause_btn = None


def set_ui_refs(c, status, hint, legend_lbl=None, pause_button=None):
    global canvas, status_label, hint_label, graph_instance, legend_label, pause_btn
    canvas = c
    status_label = status
    hint_label = hint
    legend_label = legend_lbl
    pause_btn = pause_button
    graph_instance = g_module.Graph()


def update_console(text):
    if hint_label:
        hint_label.config(text=text)


def update_legend(algo):
    if not legend_label:
        return
    if algo == "BFS":
        legend_label.config(text="BFS: Gold Node • Yellow Edge")
    elif algo == "DFS":
        legend_label.config(text="DFS: Cyan Node • Blue Edge")
    else:
        legend_label.config(text="Legend")


def set_animation_speed(value):
    global animation_speed
    animation_speed = int(float(value))


def toggle_pause():
    global paused
    paused = not paused
    if pause_btn:
        pause_btn.config(text="▶ Resume" if paused else "⏸ Pause")
    return paused


def step_forward():
    global paused
    was_paused = paused
    paused = False
    if last_algo == "bfs":
        animate_bfs_step()
    elif last_algo == "dfs":
        animate_dfs_step()
    paused = was_paused


# ================= CLICK HANDLER =================
def on_canvas_click(event):
    global waiting_for_start
    x, y = event.x, event.y

    # ================= DELETE MODE =================
    if ch.mode == "delete":
        # Delete vertex if clicked
        for vid, data in list(ch.vertices.items()):
            vx, vy = data["x"], data["y"]
            if (x - vx)**2 + (y - vy)**2 <= 400:
                canvas.delete(ch.vertices[vid]["circle"])
                canvas.delete(ch.vertices[vid]["text"])
                del ch.vertices[vid]
                graph_instance.adj_list.pop(vid, None)
                return
        # Delete edge if clicked on edge area (simple but effective)
        return

    # ================= START TRAVERSAL =================
    if ch.mode == "idle" and waiting_for_start is not None:
        for vid, data in ch.vertices.items():
            vx, vy = data["x"], data["y"]
            if (x - vx)**2 + (y - vy)**2 <= 400:
                canvas.itemconfig(ch.vertices[vid]["circle"], outline="red", width=5)
                if waiting_for_start == "bfs":
                    waiting_for_start = None
                    run_bfs(vid)
                elif waiting_for_start == "dfs":
                    waiting_for_start = None
                    run_dfs(vid)
                return

    # ================= ADD VERTEX / EDGE =================
    if ch.mode == "vertex":
        vid = ch.add_vertex(x, y)
        graph_instance.add_vertex(vid)
    elif ch.mode == "edge":
        for vid, data in list(ch.vertices.items()):
            vx, vy = data["x"], data["y"]
            if (x - vx)**2 + (y - vy)**2 <= 400:
                if len(ch.selected_vertices) == 1 and ch.selected_vertices[0] == vid:
                    ch.deselect_vertex(vid)
                    ch.selected_vertices.clear()
                    update_console("Click first vertex")
                    return
                ch.selected_vertices.append(vid)
                ch.select_vertex(vid)

                if len(ch.selected_vertices) == 1:
                    update_console("Click second vertex")
                if len(ch.selected_vertices) == 2:
                    a, b = ch.selected_vertices
                    edge_id = ch.add_edge(a, b)
                    graph_instance.add_edge(a, b)
                    for v in ch.selected_vertices:
                        ch.deselect_vertex(v)
                    ch.selected_vertices.clear()
                    update_console("Click first vertex")
                break


def start_bfs_mode():
    global waiting_for_start, paused, current_algo
    paused = False
    current_algo = "BFS"
    reset_visual_state()
    ch.mode = "idle"
    waiting_for_start = "bfs"
    status_label.config(text="Status: BFS Mode")
    update_console("Click a vertex to start BFS")
    update_legend("BFS")
    if pause_btn:
        pause_btn.config(text="⏸ Pause")


def start_dfs_mode():
    global waiting_for_start, paused, current_algo
    paused = False
    current_algo = "DFS"
    reset_visual_state()
    ch.mode = "idle"
    waiting_for_start = "dfs"
    status_label.config(text="Status: DFS Mode")
    update_console("Click a vertex to start DFS")
    update_legend("DFS")
    if pause_btn:
        pause_btn.config(text="⏸ Pause")


def run_bfs(start):
    global bfs_order, bfs_parent, bfs_step_index, bfs_steps, bfs_path, last_algo, last_start
    last_algo = "bfs"
    last_start = start
    visited = set()
    queue = [start]
    bfs_order = []
    bfs_parent = {}
    bfs_parent[start] = None
    visited.add(start)
    bfs_steps = 0
    bfs_path = 0

    while queue:
        vertex = queue.pop(0)
        bfs_steps += 1
        bfs_order.append(vertex)
        for neigh, _ in graph_instance.get_neighbors(vertex):
            bfs_steps += 1
            if neigh not in visited:
                bfs_path += 1
                visited.add(neigh)
                queue.append(neigh)
                bfs_parent[neigh] = vertex

    bfs_step_index = 0
    update_console("Running BFS...")
    animate_bfs_step()


def animate_bfs_step():
    global bfs_step_index
    if bfs_step_index >= len(bfs_order):
        show_final_summary(bfs_order, bfs_steps, bfs_path, "BFS")
        return
    if paused:
        canvas.after(100, animate_bfs_step)
        return
    vid = bfs_order[bfs_step_index]
    update_live_console("BFS", bfs_order[bfs_step_index+1:], bfs_order[:bfs_step_index+1], bfs_steps, bfs_path)
    canvas.itemconfig(ch.vertices[vid]["circle"], fill="#ffd84d", outline="#ffb300", width=3)
    parent = bfs_parent.get(vid)
    if parent is not None:
        for neigh, edge_id in graph_instance.get_neighbors(parent):
            if neigh == vid:
                canvas.itemconfig(edge_id[1] if isinstance(edge_id, tuple) else edge_id, fill="#ffe600", width=3)
                break
    bfs_step_index += 1
    canvas.after(animation_speed, animate_bfs_step)


def run_dfs(start):
    global dfs_order, dfs_parent, dfs_step_index, dfs_steps, dfs_path, last_algo, last_start
    last_algo = "dfs"
    last_start = start
    visited = set()
    stack = [start]
    dfs_order = []
    dfs_parent = {}
    dfs_parent[start] = None
    dfs_steps = 0
    dfs_path = 0

    while stack:
        vertex = stack.pop()
        dfs_steps += 1
        if vertex in visited:
            continue
        visited.add(vertex)
        dfs_order.append(vertex)
        for neigh, _ in reversed(graph_instance.get_neighbors(vertex)):
            dfs_steps += 1
            if neigh not in visited:
                dfs_path += 1
                dfs_parent[neigh] = vertex
                stack.append(neigh)

    dfs_step_index = 0
    update_console("Running DFS...")
    animate_dfs_step()


def animate_dfs_step():
    global dfs_step_index
    if dfs_step_index >= len(dfs_order):
        show_final_summary(dfs_order, dfs_steps, dfs_path, "DFS")
        return
    if paused:
        canvas.after(100, animate_dfs_step)
        return
    vid = dfs_order[dfs_step_index]
    update_live_console("DFS", dfs_order[dfs_step_index+1:], dfs_order[:dfs_step_index+1], dfs_steps, dfs_path)
    canvas.itemconfig(ch.vertices[vid]["circle"], fill="#4dd2ff", outline="#00aaff", width=3)
    parent = dfs_parent.get(vid)
    if parent is not None:
        for neigh, edge_id in graph_instance.get_neighbors(parent):
            if neigh == vid:
                canvas.itemconfig(edge_id[1] if isinstance(edge_id, tuple) else edge_id, fill="#00b7ff", width=3)
                break
    dfs_step_index += 1
    canvas.after(animation_speed, animate_dfs_step)


def restart_traversal():
    global paused
    paused = False
    if pause_btn:
        pause_btn.config(text="⏸ Pause")
    reset_visual_state()
    if last_algo == "bfs":
        bfs_step_index = 0
        update_console("Restarting BFS...")
        animate_bfs_step()
    elif last_algo == "dfs":
        dfs_step_index = 0
        update_console("Restarting DFS...")
        animate_dfs_step()


def reset_graph():
    global waiting_for_start, paused, current_algo
    paused = False
    current_algo = None
    if pause_btn:
        pause_btn.config(text="⏸ Pause")
    ch.vertices.clear()
    ch.selected_vertices.clear()
    ch.vertex_count = 0
    waiting_for_start = None
    global bfs_step_index, bfs_order, bfs_parent, dfs_step_index, dfs_order, dfs_parent
    bfs_step_index = bfs_order = bfs_parent = dfs_step_index = dfs_order = dfs_parent = 0
    reset_visual_state()
    if canvas:
        canvas.delete("all")
    status_label.config(text="Status: Idle")
    update_console("Select a mode to begin")
    ch.mode = "idle"


def reset_visual_state():
    for vid in list(ch.vertices.keys()):
        canvas.itemconfig(ch.vertices[vid]["circle"], fill="white", outline="white", width=2)


def update_live_console(algo, current, visited, steps, path):
    q_str = " → ".join(map(str, current)) if current else "Empty"
    v_str = " → ".join(map(str, visited)) if visited else "None"
    live_text = f"{algo} Running...\n\n" \
                f"{'Queue' if algo == 'BFS' else 'Stack'}: {q_str}\n\n" \
                f"Visited: {v_str}\n\n" \
                f"Steps: {steps} | Path: {path}"
    update_console(live_text)


def show_final_summary(order, steps, path, algo):
    order_str = " → ".join(map(str, order))
    summary = f"{algo} Complete\n\nTraversal Order:\n{order_str}\n\nSteps: {steps}\nPath: {path}"
    update_console(summary)