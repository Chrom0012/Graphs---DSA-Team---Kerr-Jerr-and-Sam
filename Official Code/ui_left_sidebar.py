"""
ui_left_sidebar.py
Assembles the scrollable left sidebar from its sub-modules.
"""
import tkinter as tk
import state
import ui_left_sidebar_top as top_sections
import ui_left_sidebar_bottom as bottom_sections


def build_left_sidebar(root, canvas, center_workspace_frame, pan_tip_lbl):
    container = tk.Frame(root, bg="#08090f")
    container.grid(row=1, column=0, sticky="nsew")
    container.columnconfigure(0, weight=1)
    container.columnconfigure(1, weight=0)
    container.rowconfigure(0, weight=1)

    sidebar_canvas = tk.Canvas(container, bg="#0e101a", highlightthickness=0)
    sidebar_canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar = tk.Scrollbar(container, orient="vertical",
                             command=sidebar_canvas.yview,
                             bg="#1a1c2e", troughcolor="#0e101a")
    scrollbar.grid(row=0, column=1, sticky="ns")
    sidebar_canvas.configure(yscrollcommand=scrollbar.set)

    controls = tk.Frame(sidebar_canvas, bg="#0e101a",
                        highlightthickness=1, highlightbackground="#1b1e2e")
    canvas_window = sidebar_canvas.create_window((4, 4), window=controls, anchor="nw")

    _updating = [False]

    def update_scrollregion(event=None):
        if _updating[0]:
            return
        _updating[0] = True
        try:
            sidebar_canvas.update_idletasks()
            bbox = sidebar_canvas.bbox("all")
            if bbox:
                sidebar_canvas.configure(scrollregion=bbox)
            cw = sidebar_canvas.winfo_width()
            if cw > 0:
                sidebar_canvas.itemconfig(canvas_window, width=cw - 8)
        finally:
            _updating[0] = False

    controls.bind("<Configure>", update_scrollregion)
    sidebar_canvas.bind("<Configure>", update_scrollregion)

    def on_wheel(event):
        sidebar_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    controls.bind("<Enter>", lambda e: root.bind_all("<MouseWheel>", on_wheel))
    controls.bind("<Leave>", lambda e: root.unbind_all("<MouseWheel>"))
    scrollbar.bind("<Enter>", lambda e: root.bind_all("<MouseWheel>", on_wheel))
    scrollbar.bind("<Leave>", lambda e: root.unbind_all("<MouseWheel>"))

    # ── Build all sections ────────────────────────────────────────────────────
    top_sections.build_naming_section(controls)
    play_search_btn = top_sections.build_engine_section(controls, root)
    builder_btns    = top_sections.build_builder_section(controls)
    top_sections.build_examples_section(controls, root)

    bottom_sections.build_vertex_appearance_section(controls, root, canvas)
    bottom_sections.build_canvas_bg_section(controls, root, canvas,
                                             center_workspace_frame, pan_tip_lbl)
    bottom_sections.build_edge_section(controls)
    target_setter_btn = bottom_sections.build_target_section(controls)
    bottom_sections.build_graph_type_section(controls)
    bottom_sections.build_speed_section(controls)
    bottom_sections.build_reset_section(controls)

    # ── Drawer handle ─────────────────────────────────────────────────────────
    is_left_drawer_open = [True]
    handle_strip = tk.Frame(container, bg="#111322", width=28,
                            highlightthickness=1, highlightbackground="#1b1e2e")
    handle_strip.grid(row=0, column=1, sticky="ns")
    handle_strip.pack_propagate(False)
    handle_btn = tk.Button(
        handle_strip, text="◀",
        font=("Consolas", 14, "bold"),
        fg="#00e5ff", bg="#111322",
        activebackground="#1b1e2e", activeforeground="#ffffff",
        relief="flat", bd=0
    )
    handle_btn.pack(fill="both", expand=True)

    def _initial_scroll():
        update_scrollregion()
        sidebar_canvas.yview_moveto(0)
    sidebar_canvas.after(120, _initial_scroll)

    state._left_sidebar_canvas = sidebar_canvas
    state._left_handle_btn     = handle_btn
    state._is_left_open        = is_left_drawer_open

    return {
        "container":          container,
        "controls":           controls,
        "sidebar_canvas":     sidebar_canvas,
        "play_search_btn":    play_search_btn,
        "v_btn":              builder_btns["v_btn"],
        "e_btn":              builder_btns["e_btn"],
        "m_btn":              builder_btns["m_btn"],
        "del_v_btn":          builder_btns["del_v_btn"],
        "del_e_btn":          builder_btns["del_e_btn"],
        "target_setter_btn":  target_setter_btn,
        "handle_btn":         handle_btn,
        "is_left_drawer_open": is_left_drawer_open,
    }
