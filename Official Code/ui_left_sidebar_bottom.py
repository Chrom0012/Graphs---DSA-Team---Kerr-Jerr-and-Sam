"""
ui_left_sidebar_bottom.py
Builds the bottom half of the left sidebar:
Vertex Appearance, Canvas Background, Edge Appearance,
Target Stop Vertex, Graph Type, Speed Control, Reset.
"""
import tkinter as tk
from tkinter import messagebox
import state
import graph
import ui_helpers as helpers
from ui_sidebar_widgets import CollapsibleCategory, ToolTip


def build_vertex_appearance_section(controls, root, canvas):
    cat = CollapsibleCategory(controls, "VERTEX APPEARANCE", open_by_default=True)

    color_frame = tk.Frame(cat.content, bg="#0e101a")
    color_frame.pack(fill="x", pady=4)
    color_swatch = tk.Label(color_frame, bg=state.vertex_fill_color, width=3, relief="flat")
    color_swatch.pack(side="left", padx=(0, 6), pady=2, ipady=10)
    color_pick_btn = tk.Button(
        color_frame, text="🎨 Pick Vertex Color",
        command=lambda: helpers.open_color_picker(root, color_swatch, color_pick_btn),
        font=("Consolas", 10, "bold"),
        fg=graph.get_contrast_color(state.vertex_fill_color),
        bg=state.vertex_fill_color, activebackground="#2a4a7a", relief="flat"
    )
    color_pick_btn.pack(side="left", fill="x", expand=True, ipady=6)

    # Size row
    size_mode_var = tk.StringVar(value="radius")
    size_label_frame = tk.Frame(cat.content, bg="#0e101a")
    size_label_frame.pack(fill="x", pady=(8, 2))
    tk.Label(size_label_frame, text="VERTEX SIZE:",
             font=("Consolas", 11, "bold"), fg="#8f9cae", bg="#0e101a").pack(side="left")
    toggle_frame = tk.Frame(size_label_frame, bg="#0e101a")
    toggle_frame.pack(side="right")
    r_mode_btn = tk.Button(toggle_frame, text="R", font=("Consolas", 10, "bold"),
                           bg="#00e5ff", fg="black", relief="flat", width=4)
    r_mode_btn.pack(side="left", padx=2)
    d_mode_btn = tk.Button(toggle_frame, text="D", font=("Consolas", 10, "bold"),
                           bg="#1a1c2e", fg="white", relief="flat", width=4)
    d_mode_btn.pack(side="left", padx=2)
    r_mode_btn.config(command=lambda: helpers.switch_to_radius(
        size_mode_var, size_entry, r_mode_btn, d_mode_btn, size_entry_label))
    d_mode_btn.config(command=lambda: helpers.switch_to_diameter(
        size_mode_var, size_entry, r_mode_btn, d_mode_btn, size_entry_label))

    size_input_frame = tk.Frame(cat.content, bg="#0e101a")
    size_input_frame.pack(fill="x", pady=6)
    size_entry_label = tk.Label(size_input_frame, text="R:",
                                font=("Consolas", 12, "bold"),
                                fg="#a8a8a8", bg="#0e101a", width=2)
    size_entry_label.pack(side="left")
    size_entry = tk.Entry(size_input_frame, font=("Consolas", 12),
                          bg="#1a1c2e", fg="#ffffff", insertbackground="white",
                          borderwidth=0, highlightthickness=1,
                          highlightbackground="#1b1e2e", width=6)
    size_entry.pack(side="left", padx=6, ipady=5)
    size_entry.insert(0, str(state.vertex_radius))

    slider_syncing = [False]
    size_slider = tk.Scale(
        size_input_frame, from_=5, to=60, orient="horizontal",
        bg="#0e101a", fg="#a8a8a8", troughcolor="#1a1c2e",
        highlightthickness=0, showvalue=False, length=80,
        command=lambda val: helpers.on_slider_change(
            val, size_mode_var, size_entry, slider_syncing)
    )
    size_slider.set(state.vertex_radius)
    size_slider.pack(side="left", padx=4)

    popup_items, popup_cancel_id = [], [None]
    size_set_btn = tk.Button(
        size_input_frame, text="Set",
        command=lambda: helpers.apply_vertex_size(
            size_entry, size_mode_var, size_slider,
            slider_syncing, canvas, popup_items, popup_cancel_id, controls),
        font=("Consolas", 11, "bold"), fg="white", bg="#1b1e2e",
        relief="flat", width=5
    )
    size_set_btn.pack(side="left")
    size_entry.bind("<Return>", lambda e: helpers.apply_vertex_size(
        size_entry, size_mode_var, size_slider,
        slider_syncing, canvas, popup_items, popup_cancel_id, controls))


def build_canvas_bg_section(controls, root, canvas, center_workspace_frame, pan_tip_lbl):
    cat = CollapsibleCategory(controls, "CANVAS BACKGROUND", open_by_default=True)

    canvas_color_frame = tk.Frame(cat.content, bg="#0e101a")
    canvas_color_frame.pack(fill="x", pady=4)
    canvas_color_swatch = tk.Label(canvas_color_frame, bg=state.canvas_bg_color,
                                   width=3, relief="flat")
    canvas_color_swatch.pack(side="left", padx=(0, 6), pady=2, ipady=10)
    canvas_color_btn = tk.Button(
        canvas_color_frame, text="🎨 Pick Canvas Color",
        command=lambda: helpers.open_canvas_color_picker(
            root, canvas_color_swatch, center_workspace_frame,
            canvas, pan_tip_lbl, canvas_color_btn),
        font=("Consolas", 10, "bold"),
        fg=graph.get_contrast_color(state.canvas_bg_color),
        bg=state.canvas_bg_color, activebackground="#2a4a7a", relief="flat"
    )
    canvas_color_btn.pack(side="left", fill="x", expand=True, ipady=6)

    preset_frame = tk.Frame(cat.content, bg="#0e101a")
    preset_frame.pack(fill="x", pady=6)
    for name, color in [("White", "#ffffff"), ("Dark", "#05060a"),
                         ("Navy", "#0a1628"), ("Slate", "#1a1a2e"),
                         ("Cream", "#f5f5dc"), ("Mint", "#f0fff4")]:
        btn = tk.Button(preset_frame, text="", bg=color, relief="flat", width=3,
                        command=lambda c=color: helpers.apply_canvas_preset(
                            c, canvas_color_swatch, center_workspace_frame,
                            canvas, pan_tip_lbl, canvas_color_btn))
        btn.pack(side="left", padx=2, pady=2, ipady=8)
        ToolTip(btn, name)


def build_edge_section(controls):
    cat = CollapsibleCategory(controls, "EDGE APPEARANCE", open_by_default=True)

    edge_width_frame = tk.Frame(cat.content, bg="#0e101a")
    edge_width_frame.pack(fill="x", pady=6)
    tk.Label(edge_width_frame, text="Line Width:",
             font=("Consolas", 11), fg="#a8a8a8", bg="#0e101a").pack(side="left")
    edge_width_entry = tk.Entry(edge_width_frame, font=("Consolas", 12),
                                bg="#1a1c2e", fg="#ffffff", width=6,
                                borderwidth=0, highlightthickness=1,
                                highlightbackground="#1b1e2e")
    edge_width_entry.pack(side="left", padx=6)
    edge_width_entry.insert(0, str(state.edge_width))
    edge_width_syncing = [False]
    edge_width_slider = tk.Scale(
        edge_width_frame, from_=1, to=10, orient="horizontal",
        bg="#0e101a", fg="#a8a8a8", troughcolor="#1a1c2e",
        highlightthickness=0, showvalue=False, length=80,
        command=lambda val: helpers.on_edge_width_slider(
            val, edge_width_entry, edge_width_syncing)
    )
    edge_width_slider.set(state.edge_width)
    edge_width_slider.pack(side="left", padx=4)
    tk.Button(edge_width_frame, text="Set",
              command=lambda: helpers.apply_edge_width(
                  edge_width_entry, edge_width_slider, edge_width_syncing, controls),
              font=("Consolas", 11, "bold"), fg="white", bg="#1b1e2e",
              relief="flat", width=5).pack(side="left")
    edge_width_entry.bind("<Return>", lambda e: helpers.apply_edge_width(
        edge_width_entry, edge_width_slider, edge_width_syncing, controls))


def build_target_section(controls):
    cat = CollapsibleCategory(controls, "TARGET STOP VERTEX", open_by_default=True)

    target_input_frame = tk.Frame(cat.content, bg="#0e101a")
    target_input_frame.pack(fill="x", pady=6)
    target_entry = tk.Entry(target_input_frame, font=("Consolas", 12, "bold"),
                            bg="#12131f", fg="#2ed573",
                            insertbackground="white", borderwidth=0,
                            highlightthickness=1, highlightbackground="#1b1e2e")
    target_entry.pack(side="left", fill="x", expand=True, ipady=6)
    target_setter_btn = tk.Button(
        target_input_frame, text="Lock",
        command=lambda: helpers.push_target_assignment(target_entry, controls),
        font=("Consolas", 11, "bold"), bg="#1b1e2e", fg="#2ed573", relief="flat"
    )
    target_setter_btn.pack(side="right", padx=(6, 0))
    return target_setter_btn


def build_graph_type_section(controls):
    cat = CollapsibleCategory(controls, "GRAPH TYPE", open_by_default=True)

    radio_frame = tk.Frame(cat.content, bg="#0e101a")
    radio_frame.pack(fill="x", pady=6)
    graph_type_var = tk.StringVar(value="undirected")

    def set_graph_type_with_confirm(gtype):
        if state.graph_is_not_empty():
            if not messagebox.askyesno(
                    "Confirm",
                    "Changing topology rules requires a layout clear. Proceed?"):
                graph_type_var.set(state.graph_type)
                return
        graph.reset_graph()
        graph.set_graph_type(gtype)
        graph_type_var.set(gtype)

    for label, value in (("Undirected", "undirected"), ("Directed", "directed")):
        side = "left" if value == "undirected" else "right"
        tk.Radiobutton(radio_frame, text=label,
                       variable=graph_type_var, value=value,
                       command=lambda g=value: set_graph_type_with_confirm(g),
                       font=("Consolas", 11, "bold"), fg="#ffffff",
                       bg="#0e101a", selectcolor="#1b1e2e").pack(side=side, expand=True)


def build_speed_section(controls):
    cat = CollapsibleCategory(controls, "SPEED CONTROL", open_by_default=True)

    speed_frame = tk.Frame(cat.content, bg="#0e101a")
    speed_frame.pack(fill="x", pady=6)
    tk.Label(speed_frame, text="Delay (ms):",
             font=("Consolas", 11), fg="#a8a8a8", bg="#0e101a").pack(side="left")

    def validate_numeric(P):
        return P == "" or P.isdigit()
    vcmd = (controls.register(validate_numeric), "%P")

    # FIX: only one speed_entry – previously duplicated (second was never packed, first
    # was shadowed), breaking the Set button entirely.
    speed_entry = tk.Entry(speed_frame, font=("Consolas", 12),
                           bg="#1a1c2e", fg="#ffffff", width=8,
                           borderwidth=0, highlightthickness=1,
                           highlightbackground="#1b1e2e",
                           validate="key", validatecommand=vcmd)
    speed_entry.pack(side="left", padx=6, ipady=5)
    speed_entry.insert(0, str(state.animation_speed))

    tk.Button(speed_frame, text="Set",
              command=lambda: helpers.apply_speed(speed_entry, controls),
              font=("Consolas", 11, "bold"), fg="white",
              bg="#1b1e2e", relief="flat", width=5).pack(side="left")
    speed_entry.bind("<Return>", lambda e: helpers.apply_speed(speed_entry, controls))


def build_reset_section(controls):
    cat = CollapsibleCategory(controls, "RESET", open_by_default=True)
    reset_btn = tk.Button(cat.content, text="⚠ Reset Graph Canvas",
                          command=graph.reset_graph,
                          font=("Consolas", 12, "bold"), fg="#ffffff",
                          bg="#321919", relief="flat")
    reset_btn.pack(fill="x", pady=10, ipady=8)
    helpers.apply_hover_style(reset_btn, "#321919", "#5c2424")
