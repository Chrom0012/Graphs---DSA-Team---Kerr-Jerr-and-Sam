import tkinter as tk
import graph as g


root = tk.Tk()

root.title("Graph Traversal Visualizer")
root.geometry("1920x1080")
root.configure(bg="#1f2234")
title_label = tk.Label(
    root,
    text="Graph Traversal Visualizer",
    font=("Instrument Sans", 48, "italic"),
    fg="white",
    bg="#1f2234"
)
title_label.place(x=577, y=54)

control_panel = tk.Frame(root, width=504, height=867, bg="#10111a")
control_panel.place(x=61, y=159)

control_text = tk.Label(
    control_panel,
    text="Control Panel",
    font=("42dot Sans", 36),
    fg="#a8a8a8",
    bg="#10111a"
)
control_text.place(x=45, y=25)

divider = tk.Frame(control_panel, bg="#a8a8a8", height=1, width=504)
divider.place(x=0, y=103)

algo_text = tk.Label(
    control_panel,
    text="Select Algorithm",
    font=("42dot Sans", 24),
    fg="#a8a8a8",
    bg="#10111a"
)
algo_text.place(x=140, y=150)

bfs_button = tk.Button(
    control_panel,
    text="Breadth-First Search (BFS)",
    font=("42dot Sans", 14),
    fg="#a8a8a8",
    bg="#383940",
    relief="flat",
    command=g.start_bfs_mode
)
bfs_button.place(x=44, y=190, width=416, height=61)

dfs_button = tk.Button(
    control_panel,
    text="Depth-First Search (DFS)",
    font=("42dot Sans", 14),
    fg="#a8a8a8",
    bg="#383940",
    relief="flat",
    command=g.start_dfs_mode
)
dfs_button.place(x=44, y=260, width=416, height=60)

graph_text = tk.Label(
    control_panel,
    text="Graph Controls",
    font=("42dot Sans", 24),
    fg="#a8a8a8",
    bg="#10111a"
)
graph_text.place(x=140, y=350)

divider2 = tk.Frame(control_panel, bg="#a8a8a8", height=1, width=404)
divider2.place(x=50, y=340)

add_vertex_btn = tk.Button(
    control_panel,
    text="Add Vertex",
    command=g.toggle_vertex,
    font=("42dot Sans", 14),
    fg="#a8a8a8",
    bg="#383940",
    relief="flat"
)
add_vertex_btn.place(x=44, y=390, width=416, height=61)

add_edge_btn = tk.Button(
    control_panel,
    text="Add Edge",
    command=g.toggle_edge,
    font=("42dot Sans", 14),
    fg="#a8a8a8",
    bg="#383940",
    relief="flat"
)
add_edge_btn.place(x=44, y=460, width=416, height=60)


divider3 = tk.Frame(control_panel, bg="#a8a8a8", height=1, width=404)
divider3.place(x=44, y=600)

restart_btn = tk.Button(
    control_panel,
    text="Restart Traversal",
    command=g.restart_traversal,
    font=("42dot Sans", 14),
    fg="#a8a8a8",
    bg="#383940",
    relief="flat"
)
restart_btn.place(x=44, y=680, width=416, height=61)

reset_btn = tk.Button(
    control_panel,
    text="Reset Graph",
    command=g.reset_graph,
    font=("42dot Sans", 14),
    fg="#a8a8a8",
    bg="#383940",
    relief="flat"
)
reset_btn.place(x=44, y=750, width=416, height=61)

# ================= DISPLAY PANEL =================

display_panel = tk.Frame(root, width=900, height=867, bg="#10111a")
display_panel.place(x=593, y=159)

canvas = tk.Canvas(
    display_panel,
    width=900,
    height=867,
    bg="#10111a",
    highlightthickness=0
)
canvas.pack()

console_panel = tk.Frame(root, width=350, height=867, bg="#10111a")
console_panel.place(x=1521, y=159)


console_text = tk.Label(
    console_panel,
    text="Console",
    font=("42dot Sans", 36),
    fg="#a8a8a8",
    bg="#10111a"
)
console_text.place(x=45, y=25)

# ================= STATUS =================
status_label = tk.Label(
    console_panel,
    text="Status: Idle",
    font=("42dot Sans", 18),
    fg="#a8a8a8",
    bg="#10111a"
)
status_label.place(x=20, y=140)

hint_label = tk.Label(
    console_panel,
    text="Select a mode to begin",
    font=("42dot Sans", 14),
    fg="#a8a8a8",
    bg="#10111a",
    wraplength=400,
    justify="left"
)
hint_label.place(x=20, y=200)

divider4 = tk.Frame(console_panel, bg="#a8a8a8", height=1, width=275)
divider4.place(x=38, y=103)  

g.set_ui_refs(canvas, status_label, hint_label)
canvas.bind("<Button-1>", g.on_canvas_click)
canvas.bind("<Motion>", g.on_mouse_move)

root.mainloop()
