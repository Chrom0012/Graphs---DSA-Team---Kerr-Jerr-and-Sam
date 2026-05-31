# ================= GRAPH LOGIC =================
from collections import deque
import math

mode = "idle"
vertex_count = 0
vertices = {}
selected_vertices = []
dragging_vertex = None
adj_list = {}
graph_type = "undirected"

waiting_for_start = None   # "bfs", "dfs", or None

animation_speed = 650

bfs_step_index = 0
bfs_order = []
bfs_parent = {}

dfs_step_index = 0
dfs_order = []
dfs_parent = {}

last_algo = None 
last_start = None

canvas = None
status_label = None
hint_label = None
progress_label = None
process_label = None

paused = False
step_requested = False

pause_button = None

def graph_is_not_empty():
    return len(vertices) > 0

# ================= UI SETUP =================

def set_ui_refs(c, status, hint, progress, process):
    global canvas, status_label, hint_label, progress_label, process_label
    canvas = c
    status_label = status
    hint_label = hint
    progress_label = progress
    process_label = process

def update_hint(text):
    if hint_label:
        hint_label.config(text=text)

def update_progress(text):
    if progress_label:
        progress_label.config(text=text)

def update_process(text):
    if process_label:
        process_label.config(text=text)

def set_animation_speed(value):
    global animation_speed
    animation_speed = value

def set_pause_button(btn):
    global pause_button
    pause_button = btn

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
# ================= MODE CONTROL =================

def set_mode(new_mode):
    global mode, selected_vertices, waiting_for_start

    mode = new_mode
    selected_vertices = []

    if new_mode != "idle":
        waiting_for_start = None

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
        update_process("") 


def toggle_vertex():
    set_mode("idle" if mode == "vertex" else "vertex")


def toggle_edge():
    set_mode("idle" if mode == "edge" else "edge")

def toggle_move():
    set_mode("idle" if mode == "move" else "move")


def toggle_delete():
    set_mode("idle" if mode == "delete" else "delete")

def toggle_pause():
    global paused

    paused = not paused

    if paused:
        update_hint("Traversal paused")

        if pause_button:
            pause_button.config(text="▶ Resume")

    else:
        update_hint("Traversal resumed")

        if pause_button:
            pause_button.config(text="⏸ Pause")

        resume_animation()

# ================= VISUAL HELPERS =================

def get_edge_points(x1, y1, x2, y2, r=20):
    dx = x2 - x1
    dy = y2 - y1
    dist = math.sqrt(dx*dx + dy*dy)

    if dist == 0:
        return x1, y1, x2, y2

    # unit vector
    ux = dx / dist
    uy = dy / dist

    # shorten both ends to touch circle boundary
    start_x = x1 + ux * r
    start_y = y1 + uy * r
    end_x = x2 - ux * r
    end_y = y2 - uy * r

    return start_x, start_y, end_x, end_y

def highlight_vertex(vid):
    canvas.itemconfig(vertices[vid]["circle"], outline="#00aaff", width=4)


def unhighlight_vertex(vid):
    canvas.itemconfig(vertices[vid]["circle"], outline="#6f6f6f", width=2)


def select_vertex(vid):
    canvas.itemconfig(vertices[vid]["circle"], fill="#00aaff", outline="#00aaff")


def deselect_vertex(vid):
    canvas.itemconfig(vertices[vid]["circle"], fill="white", outline="#6f6f6f")


# ================= HOVER =================

def on_mouse_move(event):
    if mode not in ["edge", "move", "delete"] and waiting_for_start is None:
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


# ================= MAIN CLICK HANDLER =================

def on_canvas_click(event):
    global vertex_count, waiting_for_start
    global dragging_vertex

    x, y = event.x, event.y

    if mode == "move":
        for vid, data in vertices.items():
            vx, vy = data["x"], data["y"]

            if (x - vx) ** 2 + (y - vy) ** 2 <= 400:
                dragging_vertex = vid
                update_hint(f"Dragging vertex {vid}")
                return
            
    # ================= DELETE MODE =================
    if mode == "delete":

        for vid, data in list(vertices.items()):
            vx, vy = data["x"], data["y"]

            if (x - vx) ** 2 + (y - vy) ** 2 <= 400:

                # remove ALL edges connected to this vertex
                for v in list(adj_list.keys()):
                    new_list = []
                    for neigh, edge_id in adj_list[v]:
                        if neigh == vid or v == vid:
                            canvas.delete(edge_id)
                        else:
                            new_list.append((neigh, edge_id))
                    adj_list[v] = new_list

                # remove vertex visuals
                canvas.delete(vertices[vid]["circle"])
                canvas.delete(vertices[vid]["text"])

                # remove from data structures
                del vertices[vid]
                del adj_list[vid]

                update_hint(f"Deleted vertex {vid}")
                return
    # ================= START BFS / DFS =================
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
            

    # ================= ADD VERTEX =================
    if mode == "vertex":

        r = 20

        circle = canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill="white",
            outline="#6f6f6f",
            width=2
        )

        text = canvas.create_text(x, y, text=str(vertex_count), fill="black")

        vertices[vertex_count] = {
            "x": x,
            "y": y,
            "circle": circle,
            "text": text
        }

        adj_list[vertex_count] = []

        vertex_count += 1


    # ================= ADD EDGE =================
    elif mode == "edge":

        for vid, data in vertices.items():

            vx, vy = data["x"], data["y"]

            if (x - vx) ** 2 + (y - vy) ** 2 <= 400:

                if len(selected_vertices) == 1 and selected_vertices[0] == vid:
                    deselect_vertex(vid)
                    selected_vertices.clear()
                    update_hint("Click first vertex")
                    return

                selected_vertices.append(vid)
                select_vertex(vid)

                if len(selected_vertices) == 1:
                    if graph_type == "directed":
                        update_hint("Click destination vertex")
                    else:
                        update_hint("Click second vertex")

                if len(selected_vertices) == 2:

                    a, b = selected_vertices

                    n1 = vertices[a]
                    n2 = vertices[b]

                    x1, y1, x2, y2 = get_edge_points(
                        n1["x"], n1["y"],
                        n2["x"], n2["y"]
                    )

                    edge = canvas.create_line(
                        x1, y1, x2, y2,
                        fill="#6f6f6f",
                        width=3,
                        tags="edge",
                        arrow="last" if graph_type == "directed" else None,
                        arrowshape=(10, 12, 4)
                    )

                    canvas.tag_lower(edge)

                    if graph_type == "undirected":
                        adj_list[a].append((b, edge))
                        adj_list[b].append((a, edge))
                    else:
                        adj_list[a].append((b, edge))

                    for vid2 in selected_vertices:
                        deselect_vertex(vid2)

                    selected_vertices.clear()
                    update_hint("Click first vertex")

                break


# ================= BFS =================

def start_bfs_mode():
    global waiting_for_start

    reset_visual_state()

    waiting_for_start = "bfs"
    set_mode("idle")

    status_label.config(text="Status: BFS Mode")
    update_hint("Click a vertex to start BFS")


def run_bfs(start):
    global bfs_order, bfs_parent, bfs_step_index
    global last_algo, last_start

    last_algo = "bfs"
    last_start = start

    visited = set()
    queue = deque()

    bfs_order = []
    bfs_parent = {}

    queue.append(start)
    visited.add(start)
    bfs_parent[start] = None

    while queue:
        vertex = queue.popleft()
        bfs_order.append(vertex)

        for neigh, _ in adj_list[vertex]:
            if neigh not in visited:
                visited.add(neigh)
                queue.append(neigh)
                bfs_parent[neigh] = vertex

    bfs_step_index = 0
    update_hint("Running BFS...")
    animate_bfs_step()


def animate_bfs_step():
    global bfs_step_index, step_requested
    
    if paused and not step_requested:
        return

    step_requested = False
    if bfs_step_index >= len(bfs_order):
        update_hint("BFS Complete")
        return

    step = bfs_step_index + 1
    vid = bfs_order[bfs_step_index]

    update_process(
        f"Step: {step}\n"
        f"Current: {vid}"
    )
    visited_so_far = bfs_order[:bfs_step_index + 1]
    visited_text = " → ".join(map(str, visited_so_far))
    update_progress(f"Traversal Order: \n{visited_text}")

    canvas.itemconfig(
        vertices[vid]["circle"],
        fill="#ffd84d",
        outline="#ffb300",
        width=3
    )

    parent = bfs_parent[vid]

    if parent is not None:
        for neigh, edge_id in adj_list[parent]:
            if neigh == vid:
                canvas.itemconfig(edge_id, fill="#ffe600", width=3)
                break

    bfs_step_index += 1
    
    if not paused:
        canvas.after(animation_speed, animate_bfs_step)


# ================= DFS =================

def start_dfs_mode():
    global waiting_for_start
    
    reset_visual_state()

    waiting_for_start = "dfs"
    set_mode("idle")

    status_label.config(text="Status: DFS Mode")
    update_hint("Click a vertex to start DFS")


def run_dfs(start):
    global dfs_order, dfs_parent, dfs_step_index
    global last_algo, last_start

    last_algo = "dfs"
    last_start = start

    visited = set()
    stack = [start]

    dfs_order = []
    dfs_parent = {}

    dfs_parent[start] = None

    while stack:
        vertex = stack.pop()

        if vertex in visited:
            continue

        visited.add(vertex)
        dfs_order.append(vertex)

        for neigh, _ in reversed(adj_list[vertex]):
            if neigh not in visited:
                dfs_parent[neigh] = vertex
                stack.append(neigh)

    dfs_step_index = 0
    update_hint("Running DFS...")
    animate_dfs_step()


def animate_dfs_step():
    global dfs_step_index, step_requested

    if paused and not step_requested:
        return

    step_requested = False

    if dfs_step_index >= len(dfs_order):
        update_hint("DFS Complete")
        return

    step = dfs_step_index + 1
    vid = dfs_order[dfs_step_index]

    update_process(
        f"Step: {step}\n"
        f"Current: {vid}"
    )
    visited_so_far = dfs_order[:dfs_step_index + 1]
    visited_text = " → ".join(map(str, visited_so_far))
    update_progress(f"Traversal Order: \n{visited_text}")

    canvas.itemconfig(
        vertices[vid]["circle"],
        fill="#4dd2ff",
        outline="#00aaff",
        width=3
    )

    parent = dfs_parent[vid]

    if parent is not None:
        for neigh, edge_id in adj_list[parent]:
            if neigh == vid:
                canvas.itemconfig(edge_id, fill="#00b7ff", width=3)
                break

    dfs_step_index += 1
    
    if not paused:
        canvas.after(animation_speed, animate_dfs_step)

# ================= RESTART =================
def restart_traversal():
    global bfs_step_index, dfs_step_index

    if last_algo is None or last_start is None:
        update_hint("No traversal to restart")
        return

    reset_visual_state()

    if last_algo == "bfs":
        bfs_step_index = 0
        update_hint("Restarting BFS...")
        animate_bfs_step()

    elif last_algo == "dfs":
        dfs_step_index = 0
        update_hint("Restarting DFS...")
        animate_dfs_step()

# ================= RESET =================

def reset_graph():
    global vertices, adj_list, vertex_count, selected_vertices
    global waiting_for_start
    global bfs_step_index, bfs_order, bfs_parent
    global dfs_step_index, dfs_order, dfs_parent

    canvas.delete("all")

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

    # 3. reset UI
    status_label.config(text="Status: Idle")
    update_hint("Select a mode to begin")
    update_progress("Traversal Order: \n")
    update_process("")
    set_mode("idle")

def reset_visual_state():
    # reset vertices
    for vid in vertices:
        canvas.itemconfig(
            vertices[vid]["circle"],
            fill="white",
            outline="#6f6f6f",
            width=2
        )

    seen = set()

    for vid in adj_list:
        for neigh, edge_id in adj_list[vid]:
            if edge_id in seen:
                continue
            seen.add(edge_id)
            canvas.itemconfig(edge_id, fill="#6f6f6f", width=3)
        
def on_canvas_drag(event):
    global dragging_vertex

    if mode != "move" or dragging_vertex is None:
        return

    x, y = event.x, event.y
    vid = dragging_vertex

    # update vertex position
    vertices[vid]["x"] = x
    vertices[vid]["y"] = y

    # move circle + text
    canvas.coords(
        vertices[vid]["circle"],
        x - 20, y - 20, x + 20, y + 20
    )

    canvas.coords(
        vertices[vid]["text"],
        x, y
    )

    for v in adj_list:
        for neigh, edge_id in adj_list[v]:

            if v == vid or neigh == vid:
                nx, ny = vertices[neigh]["x"], vertices[neigh]["y"]
                x1, y1, x2, y2 = get_edge_points(
                    vertices[v]["x"], vertices[v]["y"],
                    nx, ny
                )
                canvas.coords(edge_id, x1, y1, x2, y2)

def on_canvas_release(event):
    global dragging_vertex

    if dragging_vertex is not None:
        update_hint(f"Moved vertex {dragging_vertex}")
    dragging_vertex = None