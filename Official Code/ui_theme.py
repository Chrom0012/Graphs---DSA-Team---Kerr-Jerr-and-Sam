"""
ui_theme.py
Algo color theming, hover effects, zoom helpers, search mode triggers,
and animation-state button logic.
"""
import tkinter as tk
from tkinter import messagebox, colorchooser
import state
import graph


# ── Hover style ───────────────────────────────────────────────────────────────

def apply_hover_style(button, normal_bg, hover_bg,
                      normal_fg="white", hover_fg="white"):
    def on_enter(e):
        if button["state"] != tk.DISABLED and button.cget("bg") != "#00e5ff":
            button.config(bg=hover_bg, fg=hover_fg)
    def on_leave(e):
        if button["state"] != tk.DISABLED and button.cget("bg") != "#00e5ff":
            button.config(bg=normal_bg, fg=normal_fg)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)


# ── Algo color theme ──────────────────────────────────────────────────────────

def apply_algo_theme(color_hex):
    state.algo_color = color_hex
    for ref in ("_app_title_lbl", "_status_label", "_stats_title",
                "_frontier_box", "_progress_box"):
        widget = getattr(state, ref, None)
        if widget and widget.winfo_exists():
            try:
                widget.config(fg=color_hex)
            except Exception:
                pass
    btn = getattr(state, "_play_search_btn", None)
    if btn:
        try:
            btn.config(bg=color_hex, activebackground=color_hex)
        except Exception:
            pass


# ── Color pickers ─────────────────────────────────────────────────────────────

def open_color_picker(root, color_swatch, color_pick_btn):
    chosen = colorchooser.askcolor(color=state.vertex_fill_color,
                                   title="Pick Vertex Color", parent=root)
    if chosen and chosen[1]:
        new_color = chosen[1]
        state.vertex_fill_color = new_color
        color_swatch.config(bg=new_color)
        color_pick_btn.config(bg=new_color,
                              fg=graph.get_contrast_color(new_color))
        graph.redraw_graph()


def open_canvas_color_picker(root, canvas_color_swatch,
                             center_workspace_frame, canvas,
                             pan_tip_lbl, canvas_color_btn):
    chosen = colorchooser.askcolor(color=state.canvas_bg_color,
                                   title="Pick Canvas Background Color",
                                   parent=root)
    if chosen and chosen[1]:
        _apply_canvas_color(chosen[1], canvas_color_swatch,
                            center_workspace_frame, canvas,
                            pan_tip_lbl, canvas_color_btn)


def apply_canvas_preset(color, canvas_color_swatch,
                        center_workspace_frame, canvas,
                        pan_tip_lbl, canvas_color_btn):
    _apply_canvas_color(color, canvas_color_swatch, center_workspace_frame,
                        canvas, pan_tip_lbl, canvas_color_btn)


def _apply_canvas_color(color, swatch, frame, canvas, tip_lbl, btn):
    state.canvas_bg_color = color
    swatch.config(bg=color)
    frame.config(bg=color)
    canvas.config(bg=color)
    tip_lbl.config(bg=color, fg=graph.get_contrast_color(color))
    btn.config(bg=color, fg=graph.get_contrast_color(color))


# ── Zoom helpers ──────────────────────────────────────────────────────────────

def safe_zoom_in(canvas):
    try:
        cx = canvas.canvasx(canvas.winfo_width() / 2)
        cy = canvas.canvasy(canvas.winfo_height() / 2)
        graph.execute_ui_zoom(1.15, cx, cy)
    except Exception:
        pass


def safe_zoom_out(canvas):
    try:
        cx = canvas.canvasx(canvas.winfo_width() / 2)
        cy = canvas.canvasy(canvas.winfo_height() / 2)
        graph.execute_ui_zoom(0.85, cx, cy)
    except Exception:
        pass


# ── Search popup ──────────────────────────────────────────────────────────────

def show_search_options_popup(root, play_search_btn):
    if not state.graph_is_not_empty():
        messagebox.showwarning("Graph Empty",
                               "Cannot start search – the graph has no vertices.")
        return
    popup = tk.Menu(root, tearoff=0, bg="#111322", fg="#ffffff",
                    activebackground="#1b1e2e", activeforeground="#00e5ff",
                    font=("Consolas", 12, "bold"))
    popup.add_command(
        label=" Breadth-First Search (BFS) [Yellow] ",
        command=lambda: trigger_bfs_mode(root)
    )
    popup.add_command(
        label=" Depth-First Search (DFS) [Cyan] ",
        command=lambda: trigger_dfs_mode(root)
    )
    try:
        popup.tk_popup(
            play_search_btn.winfo_rootx(),
            play_search_btn.winfo_rooty() + play_search_btn.winfo_height()
        )
    finally:
        popup.grab_release()


def trigger_bfs_mode(root=None):
    import traversal
    apply_algo_theme("#ffd700")
    auto_open_right_drawer()
    auto_close_left_drawer()
    graph.set_mode("pick_bfs_root")
    traversal.start_bfs_mode()


def trigger_dfs_mode(root=None):
    import traversal
    apply_algo_theme("#00e5ff")
    auto_open_right_drawer()
    auto_close_left_drawer()
    graph.set_mode("pick_dfs_root")
    traversal.start_dfs_mode()


# ── Drawer helpers ────────────────────────────────────────────────────────────

def toggle_left_drawer(sidebar_canvas, root, handle_btn, is_open):
    if is_open[0]:
        sidebar_canvas.grid_remove()
        root.columnconfigure(0, weight=0, minsize=30)
        handle_btn.config(text="▶")
        is_open[0] = False
    else:
        root.columnconfigure(0, weight=16, minsize=0)
        sidebar_canvas.grid()
        handle_btn.config(text="◀")
        is_open[0] = True


def auto_open_right_drawer():
    try:
        panel = getattr(state, "_right_sidebar_panel", None)
        handle_btn = getattr(state, "_right_handle_btn", None)
        is_open = getattr(state, "_is_right_open", None)
        if panel and handle_btn and is_open is not None and not is_open[0]:
            try:
                root = panel.winfo_toplevel()
                root.columnconfigure(2, weight=11, minsize=0)
            except Exception:
                pass
            panel.grid()
            handle_btn.config(text="▶")
            is_open[0] = True
            try:
                sc = panel.winfo_children()[0]
                sc.after(50, lambda: sc.event_generate("<Configure>"))
            except Exception:
                pass
    except Exception:
        pass


def auto_close_left_drawer():
    try:
        canvas = getattr(state, "_left_sidebar_canvas", None)
        handle_btn = getattr(state, "_left_handle_btn", None)
        is_open = getattr(state, "_is_left_open", None)
        if canvas and handle_btn and is_open is not None and is_open[0]:
            root = canvas.winfo_toplevel()
            toggle_left_drawer(canvas, root, handle_btn, is_open)
    except Exception:
        pass


def auto_open_left_drawer():
    try:
        canvas = getattr(state, "_left_sidebar_canvas", None)
        handle_btn = getattr(state, "_left_handle_btn", None)
        is_open = getattr(state, "_is_left_open", None)
        if canvas and handle_btn and is_open is not None and not is_open[0]:
            root = canvas.winfo_toplevel()
            toggle_left_drawer(canvas, root, handle_btn, is_open)
    except Exception:
        pass


# ── Animation-state button logic ──────────────────────────────────────────────

def set_ui_animation_state(is_running, is_paused=False,
                           play_search_btn=None, v_btn=None, e_btn=None,
                           m_btn=None, del_v_btn=None, del_e_btn=None,
                           target_setter_btn=None, prev_btn=None,
                           step_btn=None, pause_btn=None, restart_btn=None):
    if not is_running:
        graph_mode, play_ctrl, pause_trig, action_util = (
            tk.NORMAL, tk.DISABLED, tk.DISABLED, tk.NORMAL)
    elif is_paused:
        graph_mode, play_ctrl, pause_trig, action_util = (
            tk.DISABLED, tk.NORMAL, tk.NORMAL, tk.NORMAL)
    else:
        graph_mode, play_ctrl, pause_trig, action_util = (
            tk.DISABLED, tk.DISABLED, tk.NORMAL, tk.DISABLED)

    for widget, s in [
        (play_search_btn, graph_mode), (v_btn, graph_mode),
        (e_btn, graph_mode), (m_btn, graph_mode),
        (del_v_btn, graph_mode), (del_e_btn, graph_mode),
        (target_setter_btn, graph_mode),
        (prev_btn, play_ctrl), (step_btn, play_ctrl),
        (pause_btn, pause_trig), (restart_btn, action_util),
    ]:
        if widget:
            try:
                widget.config(state=s)
            except tk.TclError:
                pass

    for tool_name, btn in {"vertex": v_btn, "edge": e_btn, "move": m_btn,
                            "delete": del_v_btn, "edge_delete": del_e_btn}.items():
        if btn:
            try:
                if not is_running and state.mode == tool_name:
                    btn.config(bg="#00e5ff", fg="black")
                else:
                    btn.config(bg="#1a1c2e", fg="white")
            except Exception:
                pass


# ── Canvas event coordinators ─────────────────────────────────────────────────

def filtered_canvas_click(event, canvas):
    event.x = canvas.canvasx(event.x)
    event.y = canvas.canvasy(event.y)
    graph.on_canvas_click(event)


def filtered_mouse_move(event, canvas):
    event.x = canvas.canvasx(event.x)
    event.y = canvas.canvasy(event.y)
    graph.on_mouse_move(event)


def filtered_canvas_drag(event, canvas):
    event.x = canvas.canvasx(event.x)
    event.y = canvas.canvasy(event.y)
    graph.on_canvas_drag(event)


def filtered_canvas_release(event, canvas):
    event.x = canvas.canvasx(event.x)
    event.y = canvas.canvasy(event.y)
    graph.on_canvas_release(event)
