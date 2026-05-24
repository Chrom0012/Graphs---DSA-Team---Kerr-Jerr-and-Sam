import tkinter as tk
import graph as g
from tkinter import messagebox

root = tk.Tk()

root.title("Graph Traversal Visualizer")
root.configure(bg="#0d0d0e")

# ================= SCALING LOGIC =================
BASE_W = 1920
BASE_H = 1080

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

root.geometry(f"{int(screen_w * 0.95)}x{int(screen_h * 0.95)}")
root.minsize(1200, 700)
root.resizable(True, True)

root.update_idletasks() 

def scale(value):
    current_w = root.winfo_width()
    current_h = root.winfo_height()
    scale_x = current_w / BASE_W
    scale_y = current_h / BASE_H
    factor = min(scale_x, scale_y)
    return max(int(value * factor), 8)
# =================================================

title_label = tk.Label(
    root,
    text="Graph Traversal Visualizer",
    font=("Instrument Sans", scale(48), "italic"),
    fg="white",
    bg="#1f2234"
)
title_label.place(x=scale(577), y=scale(54))

control_panel = tk.Frame(root, width=scale(504), height=scale(867), bg="#10111a")
control_panel.place(x=scale(61), y=scale(159))

graph_type_var = tk.StringVar(value="undirected")

control_text = tk.Label(
    control_panel,
    text="Control Panel",
    font=("42dot Sans", scale(36)),
    fg="#a8a8a8",
    bg="#10111a"
)
control_text.place(x=scale(45), y=scale(25))

divider = tk.Frame(control_panel, bg="#a8a8a8", height=1, width=scale(504))
divider.place(x=scale(0), y=scale(103))

algo_text = tk.Label(
    control_panel,
    text="Select Algorithm",
    font=("42dot Sans", scale(24)),
    fg="#a8a8a8",
    bg="#10111a"
)
algo_text.place(x=scale(140), y=scale(115))

bfs_button = tk.Button(
    control_panel,
    text="Breadth-First Search (BFS)",
    font=("42dot Sans", scale(14)),
    fg="#a8a8a8",
    bg="#383940",
    disabledforeground="#555555",
    relief="flat",
    command=g.start_bfs_mode
)
bfs_button.place(x=scale(44), y=scale(155), width=scale(416), height=scale(60))

dfs_button = tk.Button(
    control_panel,
    text="Depth-First Search (DFS)",
    font=("42dot Sans", scale(14)),
    fg="#a8a8a8",
    bg="#383940",
    disabledforeground="#555555",
    relief="flat",
    command=g.start_dfs_mode
)
dfs_button.place(x=scale(44), y=scale(225), width=scale(416), height=scale(60))

divider2 = tk.Frame(control_panel, bg="#a8a8a8", height=1, width=scale(404))
divider2.place(x=scale(50), y=scale(305))

graph_text = tk.Label(
    control_panel,
    text="Graph Controls",
    font=("42dot Sans", scale(24)),
    fg="#a8a8a8",
    bg="#10111a"
)
graph_text.place(x=scale(140), y=scale(315))

add_vertex_btn = tk.Button(
    control_panel,
    text="Add Vertex",
    command=g.toggle_vertex,
    font=("42dot Sans", scale(14)),
    fg="#a8a8a8",
    bg="#383940",
    disabledforeground="#555555",
    relief="flat"
)
add_vertex_btn.place(x=scale(44), y=scale(355), width=scale(204), height=scale(60))

add_edge_btn = tk.Button(
    control_panel,
    text="Add Edge",
    command=g.toggle_edge,
    font=("42dot Sans", scale(14)),
    fg="#a8a8a8",
    bg="#383940",
    disabledforeground="#555555",
    relief="flat"
)
add_edge_btn.place(x=scale(256), y=scale(355), width=scale(204), height=scale(60))

move_btn = tk.Button(
    control_panel,
    text="Move Vertex",
    command=g.toggle_move,
    font=("42dot Sans", scale(14)),
    fg="#a8a8a8",
    bg="#383940",
    disabledforeground="#555555",
    relief="flat"
)
move_btn.place(x=scale(44), y=scale(425), width=scale(204), height=scale(60))

delete_btn = tk.Button(
    control_panel,
    text="Delete Vertex",
    command=g.toggle_delete,
    font=("42dot Sans", scale(14)),
    fg="#a8a8a8",
    bg="#383940",
    disabledforeground="#555555",
    relief="flat"
)
delete_btn.place(x=scale(256), y=scale(425), width=scale(204), height=scale(60))

divider3 = tk.Frame(control_panel, bg="#a8a8a8", height=1, width=scale(404))
divider3.place(x=scale(50), y=scale(505))

graph_type = tk.Label(
    control_panel,
    text="Graph Type",
    font=("42dot Sans", scale(24)),
    fg="#a8a8a8",
    bg="#10111a"
)
graph_type.place(x=scale(44), y=scale(515))

def confirm_directed():
    if g.graph_is_not_empty():
        if messagebox.askyesno(
            "Change Graph Type",
            "Switching to DIRECTED will reset the graph.\n\nDo you want to continue?"
        ):
            g.reset_graph()
            graph_type_var.set("directed")
            g.set_graph_type("directed")
    else:
        graph_type_var.set("directed")
        g.set_graph_type("directed")

def confirm_undirected():
    if g.graph_is_not_empty():
        if messagebox.askyesno(
            "Change Graph Type",
            "Switching to UNDIRECTED will reset the graph.\n\nDo you want to continue?"
        ):
            g.reset_graph()
            graph_type_var.set("undirected")
            g.set_graph_type("undirected")
    else:
        graph_type_var.set("undirected")
        g.set_graph_type("undirected")

undirected_radio = tk.Radiobutton(
    control_panel,
    text="Undirected",
    variable=graph_type_var,
    value="undirected",
    command=confirm_undirected,
    font=("42dot Sans", scale(14)),
    fg="#a8a8a8",
    bg="#10111a",
    selectcolor="#383940",
    activebackground="#10111a"
)
undirected_radio.place(x=scale(220), y=scale(520))

directed_radio = tk.Radiobutton(
    control_panel,
    text="Directed",
    variable=graph_type_var,
    value="directed",
    command=confirm_directed,
    font=("42dot Sans", scale(14)),
    fg="#a8a8a8",
    bg="#10111a",
    selectcolor="#383940",
    activebackground="#10111a"
)
directed_radio.place(x=scale(360), y=scale(520))

speed_label = tk.Label(
    control_panel,
    text="Animation Speed (ms)",
    font=("42dot Sans", scale(16)),
    fg="#a8a8a8",
    bg="#10111a"
)
speed_label.place(x=scale(44), y=scale(595))

speed_entry = tk.Entry(
    control_panel,
    font=("42dot Sans", scale(14)),
    bg="#383940",
    fg="#a8a8a8",
    insertbackground="white"
)

def validate_speed_input(P):
    return P.isdigit() or P == ""

vcmd = root.register(validate_speed_input)
speed_entry.config(validate="key", validatecommand=(vcmd, "%P"))

speed_entry.place(x=scale(256), y=scale(590), width=scale(164), height=scale(40))
speed_entry.insert(0, "650")

def apply_speed():
    try:
        value = int(speed_entry.get())
        if value < 50:
            value = 50
        g.set_animation_speed(value)
        g.update_hint(f"Animation speed set to {value} ms")
    except:
        g.set_animation_speed(650)
        g.update_hint("Invalid input. Using default speed (650 ms)")
    control_panel.focus_set()

set_speed_btn = tk.Button(
    control_panel,
    text="Set",
    command=apply_speed,
    font=("42dot Sans", scale(12)),
    fg="#a8a8a8",
    bg="#383940",
    disabledforeground="#555555",
    relief="flat"
)
set_speed_btn.place(x=scale(420), y=scale(590), width=scale(40), height=scale(40))

restart_btn = tk.Button(
    control_panel,
    text="Restart Traversal",
    command=g.restart_traversal,
    font=("42dot Sans", scale(14)),
    fg="#a8a8a8",
    bg="#383940",
    disabledforeground="#555555",
    relief="flat"
)
restart_btn.place(x=scale(44), y=scale(680), width=scale(416), height=scale(61))

reset_btn = tk.Button(
    control_panel,
    text="Reset Graph",
    command=g.reset_graph,
    font=("42dot Sans", scale(14)),
    fg="#a8a8a8",
    bg="#383940",
    disabledforeground="#555555",
    relief="flat"
)
reset_btn.place(x=scale(44), y=scale(750), width=scale(416), height=scale(61))

# ================= DISPLAY PANEL =================
display_panel = tk.Frame(root, width=scale(900), height=scale(867), bg="#10111a")
display_panel.place(x=scale(593), y=scale(159))

canvas = tk.Canvas(
    display_panel,
    width=scale(900),
    height=scale(867),
    bg="#10111a",
    highlightthickness=0
)
canvas.pack()

console_panel = tk.Frame(root, width=scale(350), height=scale(867), bg="#10111a")
console_panel.place(x=scale(1521), y=scale(159))

console_text = tk.Label(
    console_panel,
    text="Console",
    font=("42dot Sans", scale(36)),
    fg="#a8a8a8",
    bg="#10111a"
)
console_text.place(x=scale(45), y=scale(25))

divider4 = tk.Frame(console_panel, bg="#a8a8a8", height=1, width=scale(275))
divider4.place(x=scale(38), y=scale(103))

# ================= STATUS & MONITORS =================
status_label = tk.Label(
    console_panel,
    text="Status: Idle",
    font=("42dot Sans", scale(18)),
    fg="#a8a8a8",
    bg="#10111a"
)
status_label.place(x=scale(20), y=scale(140))

hint_label = tk.Label(
    console_panel,
    text="Select a mode to begin",
    font=("42dot Sans", scale(14)),
    fg="#a8a8a8",
    bg="#10111a",
    wraplength=scale(300),
    justify="left"
)
hint_label.place(x=scale(20), y=scale(190))

pause_btn = tk.Button(
    console_panel,
    text="⏸ Pause",
    command=g.toggle_pause,
    font=("42dot Sans", scale(14)),
    fg="#a8a8a8",
    bg="#383940",
    disabledforeground="#555555",
    relief="flat"
)
pause_btn.place(x=scale(40), y=scale(240), width=scale(110), height=scale(50))

step_btn = tk.Button(
    console_panel,
    text="⏭ Step",
    command=g.step_forward,
    font=("42dot Sans", scale(14)),
    fg="#a8a8a8",
    bg="#383940",
    disabledforeground="#555555",
    relief="flat"
)
step_btn.place(x=scale(160), y=scale(240), width=scale(110), height=scale(50))

process_label = tk.Label(
    console_panel,
    text="",
    font=("42dot Sans", scale(14)),
    fg="#a8a8a8",
    bg="#10111a",
    justify="left",
    anchor="w"
)
process_label.place(x=scale(20), y=scale(310))

progress_label = tk.Label(
    console_panel,
    text="Traversal Order: \n",
    font=("42dot Sans", scale(14)),
    fg="#00d4ff",
    bg="#10111a",
    wraplength=scale(280),
    justify="left"
)
progress_label.place(x=scale(20), y=scale(350))

divider5 = tk.Frame(console_panel, bg="#383940", height=1, width=scale(275))
divider5.place(x=scale(38), y=scale(510))

stats_title = tk.Label(
    console_panel,
    text="Performance Statistics",
    font=("42dot Sans", scale(16), "bold"),
    fg="#ffd84d",
    bg="#10111a"
)
stats_title.place(x=scale(20), y=scale(525))

stats_label = tk.Label(
    console_panel,
    text="Time Elapsed: 0 ms\nNodes Visited: 0 / 0\nMax Structure Depth: 0",
    font=("42dot Sans", scale(13)),
    fg="#dcdcdc",
    bg="#10111a",
    justify="left"
)
stats_label.place(x=scale(20), y=scale(565))

# ================= INITIALIZE CONNECTIONS =================
g.set_ui_refs(canvas, status_label, hint_label, progress_label, process_label, stats_label)

g.set_button_refs({
    "bfs": bfs_button, "dfs": dfs_button, "vertex": add_vertex_btn,
    "edge": add_edge_btn, "move": move_btn, "delete": delete_btn,
    "undirected": undirected_radio, "directed": directed_radio,
    "speed": set_speed_btn, "restart": restart_btn, "reset": reset_btn,
    "pause": pause_btn, "step": step_btn
})

canvas.bind("<Button-1>", g.on_canvas_click)
canvas.bind("<Motion>", g.on_mouse_move)
canvas.bind("<B1-Motion>", g.on_canvas_drag)
canvas.bind("<ButtonRelease-1>", g.on_canvas_release)

root.mainloop()