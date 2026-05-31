"""
ui_left_sidebar_top.py
Builds the top half of the left sidebar:
Naming Mode, Operational Engine, Topology Builder, Quick Examples.
"""
import tkinter as tk
from tkinter import messagebox
import state
import graph
import ui_helpers as helpers
import graph_examples
from ui_sidebar_widgets import CollapsibleCategory, ToolTip


def build_naming_section(controls):
    cat = CollapsibleCategory(controls, "NAMING MODE", open_by_default=True)

    mode_frame = tk.Frame(cat.content, bg="#0e101a")
    mode_frame.pack(fill="x", pady=5)

    def switch_mode(m):
        state.vertex_naming_mode = m
        state.update_hint(f"Naming mode set to: {m.upper()}")

    for name in ("Integer", "Letter", "Custom"):
        btn = tk.Button(mode_frame, text=name,
                        command=lambda m=name.lower(): switch_mode(m),
                        bg="#1a1c2e", fg="white",
                        font=("Consolas", 10, "bold"), relief="flat")
        btn.pack(side="left", fill="x", expand=True, padx=3, ipady=4)


def build_engine_section(controls, root):
    cat = CollapsibleCategory(controls, "OPERATIONAL ENGINE", open_by_default=True)

    play_search_btn = tk.Button(
        cat.content, text="▶ Run Active Search...",
        font=("Consolas", 12, "bold"), fg="#000000", bg="#00e5ff",
        activebackground="#00bfff", relief="flat",
        command=lambda: helpers.show_search_options_popup(root, play_search_btn)
    )
    play_search_btn.pack(fill="x", pady=6, ipady=10)
    tk.Frame(cat.content, bg="#1b1e2e", height=1).pack(fill="x", pady=8)
    return play_search_btn


def build_builder_section(controls):
    cat = CollapsibleCategory(controls, "TOPOLOGY BUILDER TOOLS", open_by_default=True)

    buttons = {}
    specs = [
        ("v_btn",    "⬢ Add Vertex Node",    graph.toggle_vertex,      "#2e3456"),
        ("e_btn",    "➔ Connect Edge Link",   graph.toggle_edge,        "#2e3456"),
        ("m_btn",    "✛ Move Coordinates",    graph.toggle_move,        "#2e3456"),
        ("del_v_btn","❌ Delete Vertex Node", graph.toggle_delete,      "#ff4d4d"),
        ("del_e_btn","✂ Trim Edge Link",      graph.toggle_edge_delete, "#ff9f43"),
    ]
    for key, label, cmd, hover_bg in specs:
        btn = tk.Button(cat.content, text=label, command=cmd,
                        font=("Consolas", 11, "bold"), fg="#ffffff",
                        bg="#1a1c2e", relief="flat")
        btn.pack(fill="x", pady=4, ipady=8)
        helpers.apply_hover_style(btn, "#1a1c2e", hover_bg)
        buttons[key] = btn
    return buttons


def build_examples_section(controls, root):
    cat = CollapsibleCategory(controls, "QUICK GRAPH EXAMPLES", open_by_default=True)

    ex_frame = tk.Frame(cat.content, bg="#0e101a")
    ex_frame.pack(fill="x", pady=4)

    btn_undi = tk.Button(ex_frame, text="Undirected Triangle",
                         command=graph_examples.simple_undirected,
                         font=("Consolas", 10, "bold"), fg="white",
                         bg="#2a5a3a", relief="flat")
    btn_undi.pack(side="left", fill="x", expand=True, padx=3, ipady=6)
    helpers.apply_hover_style(btn_undi, "#2a5a3a", "#3a7a4a")

    btn_dir = tk.Button(ex_frame, text="Bidirectional Directed",
                        command=graph_examples.simple_directed,
                        font=("Consolas", 10, "bold"), fg="white",
                        bg="#5a3a2a", relief="flat")
    btn_dir.pack(side="left", fill="x", expand=True, padx=3, ipady=6)
    helpers.apply_hover_style(btn_dir, "#5a3a2a", "#7a4a3a")

    def show_random_dialog():
        d = tk.Toplevel(root)
        d.title("Random Graph Generator")
        d.geometry("340x240")
        d.configure(bg="#1a1c2e")
        d.transient(root)
        d.grab_set()
        tk.Label(d, text="Number of vertices:", fg="#00e5ff", bg="#1a1c2e",
                 font=("Consolas", 11)).pack(pady=(12, 2))
        v_entry = tk.Entry(d, bg="#2e314d", fg="white",
                           font=("Consolas", 11), width=10)
        v_entry.insert(0, "5")
        v_entry.pack(pady=2)
        tk.Label(d, text="Number of edges:", fg="#00e5ff", bg="#1a1c2e",
                 font=("Consolas", 11)).pack(pady=(8, 2))
        e_entry = tk.Entry(d, bg="#2e314d", fg="white",
                           font=("Consolas", 11), width=10)
        e_entry.insert(0, "7")
        e_entry.pack(pady=2)
        directed_var = tk.BooleanVar(value=False)
        tk.Checkbutton(d, text="Directed", variable=directed_var,
                       bg="#1a1c2e", fg="white", selectcolor="#2e3456",
                       font=("Consolas", 11)).pack(pady=5)

        def generate():
            try:
                v = int(v_entry.get())
                e = int(e_entry.get())
                graph_examples.random_graph(v, e, directed_var.get())
                d.destroy()
            except Exception:
                messagebox.showerror("Invalid input", "Please enter integers.", parent=d)

        tk.Button(d, text="Generate", command=generate,
                  bg="#00e5ff", fg="black",
                  font=("Consolas", 11, "bold"), width=14,
                  relief="flat").pack(pady=12)

    btn_random = tk.Button(cat.content, text="🎲 Random Graph...",
                           command=show_random_dialog,
                           font=("Consolas", 11, "bold"), fg="#ffffff",
                           bg="#1a1c2e", relief="flat")
    btn_random.pack(fill="x", pady=6, ipady=8)
    helpers.apply_hover_style(btn_random, "#1a1c2e", "#2e3456")
