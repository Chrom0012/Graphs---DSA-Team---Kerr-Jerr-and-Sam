import tkinter as tk
import graph as g
from tkinter import messagebox

root = tk.Tk()

root.title("Graph Traversal Visualizer")
root.geometry("1366x768")
root.configure(bg="#1f2234")
root.resizable(False, False)
root.attributes("-fullscreen", True)
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

graph_type_var = tk.StringVar(value="undirected")

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
algo_text.place(x=140, y=115)

bfs_button = tk.Button(
    control_panel,
    text="Breadth-First Search (BFS)",
    font=("42dot Sans", 14),
    fg="#a8a8a8",
    bg="#383940",
    relief="flat",
    command=g.start_bfs_mode
)
bfs_button.place(x=44, y=155, width=416, height=60)

dfs_button = tk.Button(
    control_panel,
    text="Depth-First Search (DFS)",
    font=("42dot Sans", 14),
    fg="#a8a8a8",
    bg="#383940",
    relief="flat",
    command=g.start_dfs_mode
)
dfs_button.place(x=44, y=225, width=416, height=60)

divider2 = tk.Frame(control_panel, bg="#a8a8a8", height=1, width=404)
divider2.place(x=50, y=305)

graph_text = tk.Label(
    control_panel,
    text="Graph Controls",
    font=("42dot Sans", 24),
    fg="#a8a8a8",
    bg="#10111a"
)
graph_text.place(x=140, y=315)

add_vertex_btn = tk.Button(
    control_panel,
    text="Add Vertex",
    command=g.toggle_vertex,
    font=("42dot Sans", 14),
    fg="#a8a8a8",
    bg="#383940",
    relief="flat"
)
add_vertex_btn.place(x=44, y=355, width=204, height=60)

add_edge_btn = tk.Button(
    control_panel,
    text="Add Edge",
    command=g.toggle_edge,
    font=("42dot Sans", 14),
    fg="#a8a8a8",
    bg="#383940",
    relief="flat"
)
add_edge_btn.place(x=256, y=355, width=204, height=60)

move_btn = tk.Button(
    control_panel,
    text="Move Vertex",
    command=g.toggle_move,
    font=("42dot Sans", 14),
    fg="#a8a8a8",
    bg="#383940",
    relief="flat"
)
move_btn.place(x=44, y=425, width=204, height=60)


delete_btn = tk.Button(
    control_panel,
    text="Delete Vertex",
    command=g.toggle_delete,
    font=("42dot Sans", 14),
    fg="#a8a8a8",
    bg="#383940",
    relief="flat"
)
delete_btn.place(x=256, y=425, width=204, height=60)

divider3 = tk.Frame(control_panel, bg="#a8a8a8", height=1, width=404)
divider3.place(x=50, y=505)

graph_type = tk.Label(
    control_panel,
    text="Graph Type",
    font=("42dot Sans", 24),
    fg="#a8a8a8",
    bg="#10111a"
)
graph_type.place(x=44, y=515)

# ================= GRAPH TYPE =================
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
    font=("42dot Sans", 14),
    fg="#a8a8a8",
    bg="#10111a",
    selectcolor="#383940",
    activebackground="#10111a"
)
undirected_radio.place(x=220, y=520)


directed_radio = tk.Radiobutton(
    control_panel,
    text="Directed",
    variable=graph_type_var,
    value="directed",
    command=confirm_directed,
    font=("42dot Sans", 14),
    fg="#a8a8a8",
    bg="#10111a",
    selectcolor="#383940",
    activebackground="#10111a"
)
directed_radio.place(x=360, y=520)

speed_label = tk.Label(
    control_panel,
    text="Animation Speed (ms)",
    font=("42dot Sans", 16),
    fg="#a8a8a8",
    bg="#10111a"
)
speed_label.place(x=44, y=595)

speed_entry = tk.Entry(
    control_panel,
    font=("42dot Sans", 14),
    bg="#383940",
    fg="#a8a8a8",
    insertbackground="white"
)

def validate_speed_input(P):
    return P.isdigit() or P == ""

vcmd = root.register(validate_speed_input)
speed_entry.config(validate="key", validatecommand=(vcmd, "%P"))

speed_entry.place(x=256, y=590, width=164, height=40)
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
    font=("42dot Sans", 12),
    fg="#a8a8a8",
    bg="#383940",
    relief="flat"
)
set_speed_btn.place(x=420, y=590, width=40, height=40)

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

divider4 = tk.Frame(console_panel, bg="#a8a8a8", height=1, width=275)
divider4.place(x=38, y=103)
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
hint_label.place(x=20, y=190)

progress_label = tk.Label(
    console_panel,
    text="Traversal Order: \n",
    font=("42dot Sans", 14),
    fg="#00d4ff",
    bg="#10111a",
    wraplength=300,
    justify="left"
)
progress_label.place(x=20, y=350)

process_label = tk.Label(
    console_panel,
    text="",
    font=("42dot Sans", 14),
    fg="#a8a8a8",
    bg="#10111a",
    justify="left",
    anchor="w"
)
process_label.place(x=20, y=300)

pause_btn = tk.Button(
    console_panel,
    text="⏸ Pause",
    command=g.toggle_pause,
    font=("42dot Sans", 14),
    fg="#a8a8a8",
    bg="#383940",
    relief="flat"
)
pause_btn.place(x=75, y=240, width=100, height=50)
g.set_pause_button(pause_btn)

step_btn = tk.Button(
    console_panel,
    text="⏭ Step",
    command=g.step_forward,
    font=("42dot Sans", 14),
    fg="#a8a8a8",
    bg="#383940",
    relief="flat"
)
step_btn.place(x=180, y=240, width=100, height=50)

g.set_ui_refs(canvas, status_label, hint_label, progress_label, process_label)
canvas.bind("<Button-1>", g.on_canvas_click)
canvas.bind("<Motion>", g.on_mouse_move)
canvas.bind("<B1-Motion>", g.on_canvas_drag)
canvas.bind("<ButtonRelease-1>", g.on_canvas_release)
root.mainloop()
