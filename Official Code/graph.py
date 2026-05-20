# ================= GRAPH LOGIC (Impressive Console + Live Queue/Stack) =================
print("=== GRAPH.PY LOADED SUCCESSFULLY ===")

import time

mode = "idle"
vertex_count = 0
vertices = {}
selected_vertices = []

adj_list = {}

waiting_for_start = None

bfs_step_index = 0
bfs_order = []
bfs_parent = {}
bfs_steps = 0
bfs_path = 0
bfs_start_time = 0

dfs_step_index = 0
dfs_order = []
dfs_parent = {}
dfs_steps = 0
dfs_path = 0
dfs_start_time = 0

last_algo = None 
last_start = None

canvas = None
status_label = None
hint_label = None


def set_ui_refs(c, status, hint):
    global canvas, status_label, hint_label
    canvas = c
    status_label = status
    hint_label = hint


def update_console(text):
    if hint_label:
        hint_label.config(text=text)


# ================= FINAL SUMMARY =================
def show_final_summary(order, steps, path, algo):
    order_str = " → ".join(map(str, order))
    summary = f"{algo} Complete\n\n" \
              f"Traversal Order:\n{order_str}\n\n" \
              f"Steps: {steps}\n" \
              f"Path: {path}\n\n" \
              f"Time: {time.time() - (bfs_start_time if algo == 'BFS' else dfs_start_time):.2f}s"
    update_console(summary)


# ================= LIVE CONSOLE UPDATE (BFS & DFS) =================
def update_live_console(algo, current_queue_or_stack, visited_so_far, steps, path):
    q_str = " → ".join(map(str, current_queue_or_stack)) if current_queue_or_stack else "Empty"
    v_str = " → ".join(map(str, visited_so_far)) if visited_so_far else "None"
    
    live_text = f"{algo} Running...\n\n" \
                f"{'Queue' if algo == 'BFS' else 'Stack'}: {q_str}\n\n" \
                f"Visited: {v_str}\n\n" \
                f"Steps: {steps} | Path: {path}"
    update_console(live_text)


# ================= MODE CONTROL =================
def set_mode(new_mode):
    global mode, selected_vertices, waiting_for_start
    mode = new_mode
    selected_vertices = []
    waiting_for_start = None
    reset_visual_state()

    if mode == "vertex":
        status_label.config(text="Status: Add Vertex Mode")
        update_console("Click anywhere to add vertex")
    elif mode == "edge":
        status_label.config(text="Status: Add Edge Mode")
        update_console("Click first vertex")
    else:
        status_label.config(text="Status: Idle")
        update_console("Select a mode to begin")


def toggle_vertex():
    set_mode("idle" if mode == "vertex" else "vertex")


def toggle_edge():
    set_mode("idle" if mode == "edge" else "edge")


# ================= VISUAL HELPERS (unchanged) =================
def highlight_vertex(vid):
    canvas.itemconfig(vertices[vid]["circle"], outline="lime", width=4)


def unhighlight_vertex(vid):
    canvas.itemconfig(vertices[vid]["circle"], outline="white", width=2)


def select_vertex(vid):
    canvas.itemconfig(vertices[vid]["circle"], fill="lime", outline="lime")


def deselect_vertex(vid):
    canvas.itemconfig(vertices[vid]["circle"], fill="white", outline="white")


def on_mouse_move(event):
    if mode != "edge":
        return
    x, y = event.x, event.y
    hovered = None
    for vid, data in vertices.items():
        vx, vy = data["x"], data["y"]
        if (x - vx) ** 2 + (y - vy) ** 2 <= 400:
            hovered = vid
            break

    for vid in vertices:
        if vid not in selected_vertices:
            unhighlight_vertex(vid)
    if hovered is not None and hovered not in selected_vertices:
        highlight_vertex(hovered)


# ================= CLICK HANDLER =================
def on_canvas_click(event):
    global vertex_count, waiting_for_start
    x, y = event.x, event.y

    if mode == "idle" and waiting_for_start is not None:
        for vid, data in vertices.items():
            vx, vy = data["x"], data["y"]
            if (x - vx) ** 2 + (y - vy) ** 2 <= 400:
                if waiting_for_start == "bfs":
                    waiting_for_start = None
                    run_bfs(vid)
                elif waiting_for_start == "dfs":
                    waiting_for_start = None
                    run_dfs(vid)
                return

    if mode == "vertex":
        r = 20
        circle = canvas.create_oval(x - r, y - r, x + r, y + r,
                                    fill="white", outline="white", width=2)
        text = canvas.create_text(x, y, text=str(vertex_count), fill="black")
        vertices[vertex_count] = {"x": x, "y": y, "circle": circle, "text": text}
        adj_list[vertex_count] = []
        vertex_count += 1

    elif mode == "edge":
        for vid, data in vertices.items():
            vx, vy = data["x"], data["y"]
            if (x - vx) ** 2 + (y - vy) ** 2 <= 400:
                if len(selected_vertices) == 1 and selected_vertices[0] == vid:
                    deselect_vertex(vid)
                    selected_vertices.clear()
                    update_console("Click first vertex")
                    return

                selected_vertices.append(vid)
                select_vertex(vid)

                if len(selected_vertices) == 1:
                    update_console("Click second vertex")

                if len(selected_vertices) == 2:
                    a, b = selected_vertices
                    n1 = vertices[a]
                    n2 = vertices[b]
                    edge = canvas.create_line(n1["x"], n1["y"], n2["x"], n2["y"],
                                              fill="#6f6f6f", width=3, tags="edge")
                    canvas.tag_lower(edge)

                    adj_list[a].append((b, edge))
                    adj_list[b].append((a, edge))

                    for v in selected_vertices:
                        deselect_vertex(v)
                    selected_vertices.clear()
                    update_console("Click first vertex")
                break


# ================= BFS (with live console) =================
def start_bfs_mode():
    global waiting_for_start
    reset_visual_state()
    set_mode("idle")
    waiting_for_start = "bfs"
    status_label.config(text="Status: BFS Mode")
    update_console("Click a vertex to start BFS")


def run_bfs(start):
    global bfs_order, bfs_parent, bfs_step_index, bfs_steps, bfs_path, bfs_start_time, last_algo, last_start
    last_algo = "bfs"
    last_start = start
    bfs_start_time = time.time()

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

        for neigh, _ in adj_list.get(vertex, []):
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

    vid = bfs_order[bfs_step_index]

    # Live console update
    current_queue = bfs_order[bfs_step_index+1:] + [n for n, _ in adj_list.get(vid, []) if n not in bfs_order[:bfs_step_index+1]]
    update_live_console("BFS", current_queue, bfs_order[:bfs_step_index+1], bfs_steps, bfs_path)

    # Visual highlight
    canvas.itemconfig(vertices[vid]["circle"], fill="#ffd84d", outline="#ffb300", width=3)

    parent = bfs_parent.get(vid)
    if parent is not None:
        for neigh, edge_id in adj_list.get(parent, []):
            if neigh == vid:
                canvas.itemconfig(edge_id, fill="#ffe600", width=3)
                break

    bfs_step_index += 1
    canvas.after(650, animate_bfs_step)


# ================= DFS (with live console) =================
def start_dfs_mode():
    global waiting_for_start
    reset_visual_state()
    set_mode("idle")
    waiting_for_start = "dfs"
    status_label.config(text="Status: DFS Mode")
    update_console("Click a vertex to start DFS")


def run_dfs(start):
    global dfs_order, dfs_parent, dfs_step_index, dfs_steps, dfs_path, dfs_start_time, last_algo, last_start
    last_algo = "dfs"
    last_start = start
    dfs_start_time = time.time()

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

        for neigh, _ in reversed(adj_list.get(vertex, [])):
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

    vid = dfs_order[dfs_step_index]

    # Live console update
    current_stack = dfs_order[dfs_step_index+1:] + [n for n, _ in reversed(adj_list.get(vid, [])) if n not in dfs_order[:dfs_step_index+1]]
    update_live_console("DFS", current_stack, dfs_order[:dfs_step_index+1], dfs_steps, dfs_path)

    canvas.itemconfig(vertices[vid]["circle"], fill="#4dd2ff", outline="#00aaff", width=3)

    parent = dfs_parent.get(vid)
    if parent is not None:
        for neigh, edge_id in adj_list.get(parent, []):
            if neigh == vid:
                canvas.itemconfig(edge_id, fill="#00b7ff", width=3)
                break

    dfs_step_index += 1
    canvas.after(650, animate_dfs_step)


# ================= RESTART & RESET =================
def restart_traversal():
    global bfs_step_index, dfs_step_index
    if last_algo is None or last_start is None:
        update_console("No traversal to restart")
        return

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
    global vertices, adj_list, vertex_count, selected_vertices, waiting_for_start
    global bfs_step_index, bfs_order, bfs_parent, dfs_step_index, dfs_order, dfs_parent

    vertices.clear()
    adj_list.clear()
    selected_vertices.clear()
    vertex_count = 0
    waiting_for_start = None

    bfs_step_index = 0
    bfs_order = []
    bfs_parent = {}
    dfs_step_index = 0
    dfs_order = []
    dfs_parent = {}

    reset_visual_state()
    if canvas:
        canvas.delete("all")

    status_label.config(text="Status: Idle")
    update_console("Select a mode to begin")
    set_mode("idle")


def reset_visual_state():
    for vid in list(vertices.keys()):
        canvas.itemconfig(vertices[vid]["circle"], fill="white", outline="white", width=2)
    for vid in list(adj_list.keys()):
        for _, edge_id in adj_list[vid]:
            canvas.itemconfig(edge_id, fill="#6f6f6f", width=3)