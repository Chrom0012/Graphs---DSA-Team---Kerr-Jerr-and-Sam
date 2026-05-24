import tkinter as tk
import graph as g
from tkinter import messagebox

root = tk.Tk()

root.title("Graph Traversal Visualizer Ultra Pro")
root.geometry("1366x768")
root.configure(bg="#151724") 
root.resizable(False, False)
root.attributes("-fullscreen", True)

# ================= MODERN HOVER EFFECTS FACTORY =================
def apply_hover_style(button, normal_bg, hover_bg, normal_fg="white", hover_fg="white"):
    def on_enter(e):
        if button["state"] != tk.DISABLED:
            button.config(bg=hover_bg, fg=hover_fg)
    def on_leave(e):
        if button["state"] != tk.DISABLED:
            button.config(bg=normal_bg, fg=normal_fg)
            
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

# ================= TITLE LABEL =================
title_label = tk.Label(
    root,
    text="Graph Traversal Visualizer",
    font=("Instrument Sans", 28, "italic", "bold"),
    fg="#00e5ff", 
    bg="#151724"
)
title_label.place(relx=0.5, y=30, anchor="center")

# ================= CONTROL PANEL =================
control_panel = tk.Frame(root, width=340, height=650, bg="#0b0c13", bd=0, highlightthickness=1, highlightbackground="#222538")
control_panel.place(x=20, y=85)

graph_type_var = tk.StringVar(value="undirected")

control_text = tk.Label(
    control_panel, text="Control Panel", font=("42dot Sans", 20, "bold"), fg="#ffffff", bg="#0b0c13"
)
control_text.place(x=20, y=15)

divider = tk.Frame(control_panel, bg="#222538", height=1, width=340)
divider.place(x=0, y=55)

algo_text = tk.Label(
    control_panel, text="Select Algorithm", font=("42dot Sans", 14, "bold"), fg="#a8a8a8", bg="#0b0c13"
)
algo_text.place(x=20, y=70)

bfs_button = tk.Button(
    control_panel, text="Breadth-First Search (BFS)", font=("42dot Sans", 11, "bold"),
    fg="#ffffff", bg="#222538", activebackground="#ffb300", activeforeground="black",
    disabledforeground="#444866", relief="flat", command=g.start_bfs_mode
)
bfs_button.place(x=20, y=105, width=300, height=40)
apply_hover_style(bfs_button, "#222538", "#ffd700", "white", "black")

dfs_button = tk.Button(
    control_panel, text="Depth-First Search (DFS)", font=("42dot Sans", 11, "bold"),
    fg="#ffffff", bg="#222538", activebackground="#00aaff", activeforeground="white",
    disabledforeground="#444866", relief="flat", command=g.start_dfs_mode
)
dfs_button.place(x=20, y=155, width=300, height=40)
apply_hover_style(dfs_button, "#222538", "#00e5ff", "white", "black")

divider2 = tk.Frame(control_panel, bg="#222538", height=1, width=300)
divider2.place(x=20, y=215)

graph_text = tk.Label(
    control_panel, text="Graph Controls", font=("42dot Sans", 14, "bold"), fg="#a8a8a8", bg="#0b0c13"
)
graph_text.place(x=20, y=225)

add_vertex_btn = tk.Button(
    control_panel, text="Add Vertex", command=g.toggle_vertex, font=("42dot Sans", 11, "bold"),
    fg="#ffffff", bg="#1a1c2e", disabledforeground="#444866", relief="flat"
)
add_vertex_btn.place(x=20, y=260, width=145, height=40)
apply_hover_style(add_vertex_btn, "#1a1c2e", "#2e3456")

add_edge_btn = tk.Button(
    control_panel, text="Add Edge", command=g.toggle_edge, font=("42dot Sans", 11, "bold"),
    fg="#ffffff", bg="#1a1c2e", disabledforeground="#444866", relief="flat"
)
add_edge_btn.place(x=175, y=260, width=145, height=40)
apply_hover_style(add_edge_btn, "#1a1c2e", "#2e3456")

move_btn = tk.Button(
    control_panel, text="Move Vertex", command=g.toggle_move, font=("42dot Sans", 11, "bold"),
    fg="#ffffff", bg="#1a1c2e", disabledforeground="#444866", relief="flat"
)
move_btn.place(x=20, y=310, width=145, height=40)
apply_hover_style(move_btn, "#1a1c2e", "#2e3456")

delete_btn = tk.Button(
    control_panel, text="Delete Vertex", command=g.toggle_delete, font=("42dot Sans", 11, "bold"),
    fg="#ffffff", bg="#1a1c2e", disabledforeground="#444866", relief="flat"
)
delete_btn.place(x=175, y=310, width=145, height=40)
apply_hover_style(delete_btn, "#1a1c2e", "#ff4444", "white", "white")

divider3 = tk.Frame(control_panel, bg="#222538", height=1, width=300)
divider3.place(x=20, y=370)

graph_type = tk.Label(
    control_panel, text="Graph Type", font=("42dot Sans", 14, "bold"), fg="#a8a8a8", bg="#0b0c13"
)
graph_type.place(x=20, y=380)

def confirm_directed():
    if g.graph_is_not_empty():
        if messagebox.askyesno("Change Graph Type", "Switching to DIRECTED will reset the graph.\n\nContinue?"):
            g.reset_graph()
            graph_type_var.set("directed")
            g.set_graph_type("directed")
    else:
        graph_type_var.set("directed")
        g.set_graph_type("directed")

def confirm_undirected():
    if g.graph_is_not_empty():
        if messagebox.askyesno("Change Graph Type", "Switching to UNDIRECTED will reset the graph.\n\nContinue?"):
            g.reset_graph()
            graph_type_var.set("undirected")
            g.set_graph_type("undirected")
    else:
        graph_type_var.set("undirected")
        g.set_graph_type("undirected")

undirected_radio = tk.Radiobutton(
    control_panel, text="Undirected", variable=graph_type_var, value="undirected",
    command=confirm_undirected, font=("42dot Sans", 11), fg="#ffffff", bg="#0b0c13",
    selectcolor="#222538", activebackground="#0b0c13", activeforeground="white"
)
undirected_radio.place(x=135, y=383)

directed_radio = tk.Radiobutton(
    control_panel, text="Directed", variable=graph_type_var, value="directed",
    command=confirm_directed, font=("42dot Sans", 11), fg="#ffffff", bg="#0b0c13",
    selectcolor="#222538", activebackground="#0b0c13", activeforeground="white"
)
directed_radio.place(x=240, y=383)

speed_label = tk.Label(
    control_panel, text="Speed (ms)", font=("42dot Sans", 12), fg="#a8a8a8", bg="#0b0c13"
)
speed_label.place(x=20, y=435)

speed_entry = tk.Entry(
    control_panel, font=("42dot Sans", 12), bg="#1a1c2e", fg="#ffffff",
    insertbackground="white", borderwidth=0, highlightthickness=1, highlightbackground="#222538"
)
vcmd = root.register(lambda P: P.isdigit() or P == "")
speed_entry.config(validate="key", validatecommand=(vcmd, "%P"))
speed_entry.place(x=190, y=433, width=80, height=30)
speed_entry.insert(0, "650")

def apply_speed():
    try:
        value = int(speed_entry.get())
        if value < 50: value = 50
        g.set_animation_speed(value)
        g.update_hint(f"Speed configured to {value} ms")
    except:
        g.set_animation_speed(650)
        g.update_hint("Default speed loaded (650 ms)")
    control_panel.focus_set()

set_speed_btn = tk.Button(
    control_panel, text="Set", command=apply_speed, font=("42dot Sans", 10, "bold"),
    fg="#ffffff", bg="#222538", relief="flat"
)
set_speed_btn.place(x=280, y=433, width=40, height=30)
apply_hover_style(set_speed_btn, "#222538", "#2e3456")

# Shifted clean system reset upwards to close layout gap gracefully
reset_btn = tk.Button(
    control_panel, text="Reset Graph System", command=g.reset_graph,
    font=("42dot Sans", 12, "bold"), fg="#ffffff", bg="#2c1a1a", relief="flat"
)
reset_btn.place(x=20, y=490, width=300, height=45)
apply_hover_style(reset_btn, "#2c1a1a", "#522424")


# ================= CANVAS DISPLAY PANEL =================
display_panel = tk.Frame(root, width=640, height=650, bg="#0b0c13", highlightthickness=1, highlightbackground="#222538")
display_panel.place(x=380, y=85)

canvas = tk.Canvas(display_panel, width=640, height=650, bg="#0b0c13", highlightthickness=0, scrollregion=(-3000, -3000, 3000, 3000))
canvas.pack()

btn_zoom_in = tk.Button(display_panel, text="[ + ] Zoom In", font=("42dot Sans", 10, "bold"), bg="#1a1c2e", fg="white", relief="flat", command=lambda: g.execute_ui_zoom(1.15, 320, 325))
btn_zoom_in.place(x=420, y=15, width=100, height=30)
apply_hover_style(btn_zoom_in, "#1a1c2e", "#00e5ff", "white", "black")

btn_zoom_out = tk.Button(display_panel, text="[ - ] Zoom Out", font=("42dot Sans", 10, "bold"), bg="#1a1c2e", fg="white", relief="flat", command=lambda: g.execute_ui_zoom(0.85, 320, 325))
btn_zoom_out.place(x=525, y=15, width=100, height=30)
apply_hover_style(btn_zoom_out, "#1a1c2e", "#00e5ff", "white", "black")

pan_hint = tk.Label(display_panel, text="💡 Right-Click Drag to Pan | Scroll Wheel to Zoom", font=("42dot Sans", 9), fg="#646882", bg="#0b0c13")
pan_hint.place(x=10, y=625)


# ================= CONSOLE PANEL =================
console_panel = tk.Frame(root, width=306, height=650, bg="#0b0c13", highlightthickness=1, highlightbackground="#222538")
console_panel.place(x=1040, y=85)

console_text_lbl = tk.Label(
    console_panel, text="Console", font=("42dot Sans", 20, "bold"), fg="#ffffff", bg="#0b0c13"
)
console_text_lbl.place(x=20, y=15)

divider4 = tk.Frame(console_panel, bg="#222538", height=1, width=306)
divider4.place(x=0, y=55)

status_label = tk.Label(
    console_panel, text="Status: Idle", font=("42dot Sans", 12, "bold"), fg="#a8a8a8", bg="#0b0c13"
)
status_label.place(x=20, y=65)

hint_label = tk.Label(
    console_panel, text="Select a mode to begin", font=("42dot Sans", 11),
    fg="#00e5ff", bg="#0b0c13", wraplength=260, justify="left"
)
hint_label.place(x=20, y=95)

# --- PLAYBACK STACK CONTROL CLUSTER ---
prev_btn = tk.Button(
    console_panel, text="⏮ Prev", command=g.step_backward,
    font=("42dot Sans", 10, "bold"), fg="#ffffff", bg="#222538", relief="flat", state=tk.DISABLED
)
prev_btn.place(x=15, y=145, width=85, height=35)
apply_hover_style(prev_btn, "#222538", "#2e3456")

pause_btn = tk.Button(
    console_panel, text="⏸ Pause", command=g.toggle_pause,
    font=("42dot Sans", 10, "bold"), fg="#ffffff", bg="#222538", relief="flat", state=tk.DISABLED
)
pause_btn.place(x=110, y=145, width=85, height=35)
apply_hover_style(pause_btn, "#222538", "#2e3456")

step_btn = tk.Button(
    console_panel, text="Next ⏭", command=g.step_forward,
    font=("42dot Sans", 10, "bold"), fg="#ffffff", bg="#222538", relief="flat", state=tk.DISABLED
)
step_btn.place(x=205, y=145, width=85, height=35)
apply_hover_style(step_btn, "#222538", "#2e3456")

# Shifted Restart Traversal here dynamically to tie directly with the manual execution buttons
restart_btn = tk.Button(
    console_panel, text="🔄 Restart Traversal", command=g.restart_traversal,
    font=("42dot Sans", 11, "bold"), fg="#ffffff", bg="#1a1c2e", relief="flat", state=tk.DISABLED
)
restart_btn.place(x=15, y=190, width=275, height=35)
apply_hover_style(restart_btn, "#1a1c2e", "#2e3456")

# Shifting display tracks downward cleanly to maintain pixel-perfect distribution
process_label = tk.Label(
    console_panel, text="", font=("42dot Sans", 11, "bold"), fg="#ffffff", bg="#0b0c13"
)
process_label.place(x=20, y=240)

order_title = tk.Label(
    console_panel, text="Traversal Order:", font=("42dot Sans", 11, "bold"), fg="#a8a8a8", bg="#0b0c13"
)
order_title.place(x=20, y=265)

progress_box = tk.Text(
    console_panel, font=("Consolas", 11, "bold"), bg="#12131f", fg="#ffd700",
    wrap="word", borderwidth=0, highlightthickness=1, highlightbackground="#222538", state="disabled"
)
progress_box.place(x=20, y=290, width=245, height=175)

scrollbar_y = tk.Scrollbar(console_panel, orient="vertical", command=progress_box.yview)
scrollbar_y.place(x=265, y=290, width=18, height=175)
progress_box.config(yscrollcommand=scrollbar_y.set)

# ================= PERFORMANCE STATS PANEL =================
divider5 = tk.Frame(console_panel, bg="#222538", height=1, width=266)
divider5.place(x=20, y=485)

stats_title = tk.Label(
    console_panel, text="Performance Statistics", font=("42dot Sans", 13, "bold"), fg="#ffd700", bg="#0b0c13"
)
stats_title.place(x=20, y=495)

stats_label = tk.Label(
    console_panel, text="Time Elapsed: 0 ms\nNodes Visited: 0 / 0\nMax Structure Depth: 0",
    font=("42dot Sans", 11), fg="#dcdcdc", bg="#0b0c13", justify="left"
)
stats_label.place(x=20, y=530)


# ================= FINE-TUNED STATE ENGINE INTERLOCK =================
def set_ui_animation_state(is_running, is_paused=False):
    if not is_running:
        graph_modifiers = tk.NORMAL
        playback_controls = tk.DISABLED
        pause_trigger = tk.DISABLED
        action_utilities = tk.NORMAL
    else:
        if is_paused:
            graph_modifiers = tk.DISABLED
            playback_controls = tk.NORMAL
            pause_trigger = tk.NORMAL
            action_utilities = tk.NORMAL
        else:
            graph_modifiers = tk.DISABLED
            playback_controls = tk.DISABLED
            pause_trigger = tk.NORMAL
            action_utilities = tk.DISABLED

    bfs_button.config(state=graph_modifiers)
    dfs_button.config(state=graph_modifiers)
    add_vertex_btn.config(state=graph_modifiers)
    add_edge_btn.config(state=graph_modifiers)
    move_btn.config(state=graph_modifiers)
    delete_btn.config(state=graph_modifiers)
    undirected_radio.config(state=graph_modifiers)
    directed_radio.config(state=graph_modifiers)
    set_speed_btn.config(state=graph_modifiers)
    
    prev_btn.config(state=playback_controls)
    step_btn.config(state=playback_controls)
    pause_btn.config(state=pause_trigger)
    
    restart_btn.config(state=action_utilities)
    reset_btn.config(state=action_utilities)

g.set_ui_animation_state = set_ui_animation_state

# ================= INITIALIZE FRAMEWORK SYSTEM =================
g.set_ui_refs(canvas, status_label, hint_label, progress_box, process_label, stats_label)

g.set_button_refs({
    "bfs": bfs_button, "dfs": dfs_button, "vertex": add_vertex_btn,
    "edge": add_edge_btn, "move": move_btn, "delete": delete_btn,
    "undirected": undirected_radio, "directed": directed_radio,
    "speed": set_speed_btn, "restart": restart_btn, "reset": reset_btn,
    "previous": prev_btn, "pause": pause_btn, "step": step_btn
})

canvas.bind("<Button-1>", g.on_canvas_click)
canvas.bind("<Motion>", g.on_mouse_move)
canvas.bind("<B1-Motion>", g.on_canvas_drag)
canvas.bind("<ButtonRelease-1>", g.on_canvas_release)

canvas.bind("<Button-2>", g.start_canvas_pan) 
canvas.bind("<B2-Motion>", g.drag_canvas_pan)
canvas.bind("<Button-3>", g.start_canvas_pan) 
canvas.bind("<B3-Motion>", g.drag_canvas_pan)

canvas.bind("<MouseWheel>", g.handle_mouse_wheel_zoom)

root.mainloop()