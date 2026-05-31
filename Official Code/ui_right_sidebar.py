"""
ui_right_sidebar.py
Right diagnostic sidebar: scrollable console panel with playback controls,
frontier display, adjacency list, and stats.
"""
import tkinter as tk
import state
import traversal


def _build_scrollable_panel(root, container):
    """Returns (right_panel, scroll_canvas, console, update_scrollregion)."""
    right_panel = tk.Frame(container, bg="#0e101a")
    right_panel.grid(row=0, column=1, sticky="nsew")
    right_panel.columnconfigure(0, weight=1)
    right_panel.rowconfigure(0, weight=1)

    scroll_canvas = tk.Canvas(right_panel, bg="#0e101a", highlightthickness=0)
    scroll_canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar = tk.Scrollbar(right_panel, orient="vertical",
                             command=scroll_canvas.yview,
                             bg="#1a1c2e", troughcolor="#0e101a")
    scrollbar.grid(row=0, column=1, sticky="ns")
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    console = tk.Frame(scroll_canvas, bg="#0e101a",
                       highlightthickness=1, highlightbackground="#1b1e2e")
    canvas_window = scroll_canvas.create_window((0, 0), window=console, anchor="nw")

    _updating = [False]

    def update_scrollregion(event=None):
        if _updating[0]:
            return
        _updating[0] = True
        try:
            scroll_canvas.update_idletasks()
            bbox = scroll_canvas.bbox("all")
            if bbox:
                scroll_canvas.configure(scrollregion=bbox)
            cw = scroll_canvas.winfo_width()
            if cw > 0:
                scroll_canvas.itemconfig(canvas_window, width=cw)
        finally:
            _updating[0] = False

    def _on_console_configure(event):
        hint_label_ref[0].config(wraplength=max(110, event.width - 30))
        update_scrollregion(event)

    hint_label_ref = [None]   # filled after hint_label is created
    console.bind("<Configure>", _on_console_configure)
    scroll_canvas.bind("<Configure>", update_scrollregion)

    def on_wheel(event):
        scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"
    console.bind("<Enter>",  lambda e: root.bind_all("<MouseWheel>", on_wheel))
    console.bind("<Leave>",  lambda e: root.unbind_all("<MouseWheel>"))
    scrollbar.bind("<Enter>", lambda e: root.bind_all("<MouseWheel>", on_wheel))
    scrollbar.bind("<Leave>", lambda e: root.unbind_all("<MouseWheel>"))

    return right_panel, scroll_canvas, console, update_scrollregion, hint_label_ref


def _build_console_content(console):
    """Populate console with all diagnostic widgets; return widget refs."""
    tk.Label(console, text="DIAGNOSTIC ARCHITECTURE",
             font=("Consolas", 13, "bold"), fg="#8f9cae", bg="#0e101a"
             ).pack(anchor="w", padx=15, pady=(18, 6))

    status_label = tk.Label(console, text="Status: Idle",
                            font=("Consolas", 12, "bold"),
                            fg="#a8a8a8", bg="#0e101a")
    status_label.pack(anchor="w", padx=15, pady=4)

    hint_label = tk.Label(console,
                          text="Select a mode to begin custom engineering.",
                          font=("Consolas", 12), fg="#00e5ff", bg="#0e101a",
                          justify="left")
    hint_label.pack(anchor="w", padx=15, pady=(2, 10), fill="x")

    # Playback controls
    playback_frame = tk.Frame(console, bg="#0e101a")
    playback_frame.pack(fill="x", padx=12, pady=6)

    def _pb_btn(text, cmd):
        return tk.Button(playback_frame, text=text, command=cmd,
                         font=("Consolas", 16, "bold"),
                         fg="#ffffff", bg="#1b1e2e", relief="flat",
                         state=tk.DISABLED)

    prev_btn    = _pb_btn("⏮", traversal.step_backward)
    pause_btn   = _pb_btn("⏸", traversal.toggle_pause)
    step_btn    = _pb_btn("⏭", traversal.step_forward)
    restart_btn = tk.Button(playback_frame, text="🔄",
                            command=traversal.restart_traversal,
                            font=("Consolas", 16, "bold"),
                            fg="#ffffff", bg="#16192e", relief="flat",
                            state=tk.DISABLED)
    for btn in (prev_btn, pause_btn, step_btn, restart_btn):
        btn.pack(side="left", fill="x", expand=True, padx=2, ipady=5)

    process_label = tk.Label(console, text="Step Index: 0",
                             font=("Consolas", 12, "bold"),
                             fg="#ffffff", bg="#0e101a")
    process_label.pack(anchor="w", padx=15, pady=(10, 4))

    def _section_label(text):
        tk.Label(console, text=text, font=("Consolas", 11, "bold"),
                 fg="#8f9cae", bg="#0e101a").pack(anchor="w", padx=15, pady=(6, 2))

    def _text_box(height):
        t = tk.Text(console, font=("Consolas", 12, "bold"),
                    bg="#12131f", fg="#00e5ff", borderwidth=0,
                    highlightthickness=1, highlightbackground="#1b1e2e",
                    height=height, state="disabled", wrap="word")
        t.pack(fill="x", padx=15, pady=4)
        return t

    _section_label("DATA STRUCTURE FRONTIER:")
    frontier_box = _text_box(2)

    _section_label("TRACE ROADMAP PROGRESS:")
    progress_box = _text_box(3)

    _section_label("LIVE ADJACENCY LIST VIEW:")
    adj_text_widget = tk.Text(console, font=("Consolas", 11),
                              bg="#090a10", fg="#a8b2c1", borderwidth=0,
                              highlightthickness=1, highlightbackground="#1b1e2e",
                              height=5, state="disabled", wrap="word")
    adj_text_widget.pack(fill="x", padx=15, pady=4)

    stats_title = tk.Label(console, text="PERFORMANCE STATISTICS",
                           font=("Consolas", 12, "bold"),
                           fg="#ffd700", bg="#0e101a")
    stats_title.pack(anchor="w", padx=15, pady=(14, 4))

    stats_label = tk.Label(
        console,
        text="⏱ Time Elapsed: 0 ms\n⬢ Nodes Visited: 0 / 0\n🪵 Step Counter: #0",
        font=("Consolas", 12, "bold"), fg="#dcdcdc", bg="#0e101a", justify="left"
    )
    stats_label.pack(anchor="w", padx=15, pady=5)

    return dict(
        status_label=status_label, hint_label=hint_label,
        process_label=process_label, frontier_box=frontier_box,
        progress_box=progress_box, adj_text_widget=adj_text_widget,
        stats_title=stats_title, stats_label=stats_label,
        prev_btn=prev_btn, pause_btn=pause_btn,
        step_btn=step_btn, restart_btn=restart_btn,
    )


def build_right_sidebar(root):
    container = tk.Frame(root, bg="#08090f")
    container.grid(row=1, column=2, sticky="nsew")
    container.columnconfigure(0, weight=0)
    container.columnconfigure(1, weight=1)
    container.rowconfigure(0, weight=1)

    (right_panel, scroll_canvas, console,
     update_scrollregion, hint_label_ref) = _build_scrollable_panel(root, container)

    widgets = _build_console_content(console)
    hint_label_ref[0] = widgets["hint_label"]   # wire up wraplength callback

    # ── Drawer handle ─────────────────────────────────────────────────────────
    handle_strip = tk.Frame(container, bg="#111322", width=28,
                            highlightthickness=1, highlightbackground="#1b1e2e")
    handle_strip.grid(row=0, column=0, sticky="ns")
    handle_strip.pack_propagate(False)

    handle_btn = tk.Button(handle_strip, text="◀",
                           font=("Consolas", 14, "bold"),
                           fg="#00e5ff", bg="#111322",
                           activebackground="#1b1e2e", activeforeground="#ffffff",
                           relief="flat", bd=0)
    handle_btn.pack(fill="both", expand=True)

    right_panel.grid_remove()
    root.columnconfigure(2, weight=0, minsize=30)
    is_right_drawer_open = [False]

    def toggle_right_drawer():
        if is_right_drawer_open[0]:
            right_panel.grid_remove()
            root.columnconfigure(2, weight=0, minsize=30)
            handle_btn.config(text="◀")
            is_right_drawer_open[0] = False
        else:
            root.columnconfigure(2, weight=11, minsize=0)
            right_panel.grid()
            handle_btn.config(text="▶")
            is_right_drawer_open[0] = True
            scroll_canvas.after(50, update_scrollregion)

    handle_btn.config(command=toggle_right_drawer)

    # Expose refs to state for auto-open helpers
    state._right_sidebar_panel   = right_panel
    state._right_sidebar_console = console
    state._right_handle_btn      = handle_btn
    state._is_right_open         = is_right_drawer_open

    scroll_canvas.after(120, update_scrollregion)

    return dict(
        container=container, console=console,
        handle_btn=handle_btn,
        is_right_drawer_open=is_right_drawer_open,
        **widgets,
    )
