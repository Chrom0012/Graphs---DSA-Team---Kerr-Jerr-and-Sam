import tkinter as tk
import graph as g   # <-- your groupmate's file

# ====================== RESPONSIVE WINDOW ======================
root = tk.Tk()
root.title("Graph Traversal Visualizer")
root.configure(bg="#1f2234")

BASE_W = 1920
BASE_H = 1080

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

root.geometry(f"{int(screen_w * 0.95)}x{int(screen_h * 0.95)}")
root.minsize(1200, 700)
root.resizable(True, True)

def scale(value):
    current_w = root.winfo_width()
    current_h = root.winfo_height()
    scale_x = current_w / BASE_W
    scale_y = current_h / BASE_H
    factor = min(scale_x, scale_y)
    return max(int(value * factor), 8)

# Grid layout
root.columnconfigure(0, weight=24, uniform="main")
root.columnconfigure(1, weight=55, uniform="main")
root.columnconfigure(2, weight=21, uniform="main")
root.rowconfigure(1, weight=1)

# ================= TITLE =================
title_label = tk.Label(
    root, text="Graph Traversal Visualizer",
    fg="white", bg="#1f2234"
)
title_label.grid(row=0, column=0, columnspan=3, pady=(20, 10), sticky="ew")

# ================= PANELS =================
control_panel = tk.Frame(root, bg="#10111a")
control_panel.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=(10, 20))
control_panel.grid_columnconfigure(0, weight=1)

display_panel = tk.Frame(root, bg="#10111a")
display_panel.grid(row=1, column=1, sticky="nsew", padx=10, pady=(10, 20))
display_panel.grid_columnconfigure(0, weight=1)
display_panel.grid_rowconfigure(0, weight=1)

console_panel = tk.Frame(root, bg="#10111a")
console_panel.grid(row=1, column=2, sticky="nsew", padx=(10, 20), pady=(10, 20))

# ================= CONTROL PANEL =================
control_text = tk.Label(control_panel, text="Control Panel", fg="#a8a8a8", bg="#10111a")
control_text.grid(row=0, column=0, pady=(20, 10), sticky="ew")

divider = tk.Frame(control_panel, bg="#a8a8a8", height=1)
divider.grid(row=1, column=0, sticky="ew", pady=(0, 20))

algo_text = tk.Label(control_panel, text="Select Algorithm", fg="#a8a8a8", bg="#10111a")
algo_text.grid(row=2, column=0, pady=(0, 12), sticky="ew")

bfs_button = tk.Button(
    control_panel, text="Breadth-First Search (BFS)",
    command=g.start_bfs_mode,
    fg="#a8a8a8", bg="#383940", relief="flat"
)
bfs_button.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 8))

dfs_button = tk.Button(
    control_panel, text="Depth-First Search (DFS)",
    command=g.start_dfs_mode,
    fg="#a8a8a8", bg="#383940", relief="flat"
)
dfs_button.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 18))

divider2 = tk.Frame(control_panel, bg="#a8a8a8", height=1)
divider2.grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 18))

graph_text = tk.Label(control_panel, text="Graph Controls", fg="#a8a8a8", bg="#10111a")
graph_text.grid(row=6, column=0, pady=(0, 12), sticky="ew")

add_vertex_btn = tk.Button(
    control_panel, text="Add Vertex",
    command=g.toggle_vertex,
    fg="#a8a8a8", bg="#383940", relief="flat"
)
add_vertex_btn.grid(row=7, column=0, sticky="ew", padx=20, pady=(0, 8))

add_edge_btn = tk.Button(
    control_panel, text="Add Edge",
    command=g.toggle_edge,
    fg="#a8a8a8", bg="#383940", relief="flat"
)
add_edge_btn.grid(row=8, column=0, sticky="ew", padx=20, pady=(0, 18))

# Restart & Reset
control_panel.grid_rowconfigure(9, weight=1)

restart_btn = tk.Button(
    control_panel, text="Restart Traversal",
    command=g.restart_traversal,
    fg="#a8a8a8", bg="#383940", relief="flat"
)
restart_btn.grid(row=10, column=0, sticky="ew", padx=20, pady=(0, 8))

reset_btn = tk.Button(
    control_panel, text="Reset Graph",
    command=g.reset_graph,
    fg="#a8a8a8", bg="#383940", relief="flat"
)
reset_btn.grid(row=11, column=0, sticky="ew", padx=20, pady=(0, 20))

# ================= CANVAS =================
canvas = tk.Canvas(display_panel, bg="#10111a", highlightthickness=0)
canvas.grid(row=0, column=0, sticky="nsew")

# ================= CONSOLE =================
console_text = tk.Label(console_panel, text="Console", fg="#a8a8a8", bg="#10111a")
console_text.grid(row=0, column=0, pady=(20, 10), sticky="ew")

status_label = tk.Label(console_panel, text="Status: Idle", fg="#a8a8a8", bg="#10111a")
status_label.grid(row=1, column=0, sticky="w", padx=20, pady=(10, 6))

hint_label = tk.Label(
    console_panel, text="Select a mode to begin",
    fg="#a8a8a8", bg="#10111a", justify="left", wraplength=300
)
hint_label.grid(row=2, column=0, sticky="w", padx=20)

# ================= SETUP =================
g.set_ui_refs(canvas, status_label, hint_label)
canvas.bind("<Button-1>", g.on_canvas_click)
canvas.bind("<Motion>", g.on_mouse_move)

# ================= RESPONSIVE FONTS =================
def update_ui(event=None):
    title_label.config(font=("Instrument Sans", scale(48), "italic"))
    control_text.config(font=("42dot Sans", scale(36)))
    algo_text.config(font=("42dot Sans", scale(24)))
    graph_text.config(font=("42dot Sans", scale(24)))
    console_text.config(font=("42dot Sans", scale(36)))

    btn_font = ("42dot Sans", scale(14))
    for btn in (bfs_button, dfs_button, add_vertex_btn, add_edge_btn, restart_btn, reset_btn):
        btn.config(font=btn_font)

    status_label.config(font=("42dot Sans", scale(18)))
    hint_label.config(font=("42dot Sans", scale(14)))

root.bind("<Configure>", update_ui)
root.update_idletasks()
update_ui()

root.mainloop()