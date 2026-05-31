import sys
import tkinter as tk
import state
import graph
import traversal
import ui_helpers as helpers
import ui_left_sidebar
import ui_right_sidebar
import ui_canvas


def _apply_dpi_scaling(root):
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            try:
                import ctypes
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass
    try:
        root.update_idletasks()
        dpi = root.winfo_fpixels('1i')
        if dpi < 72:
            dpi = 96.0
        scale = dpi / 72.0
        root.tk.call('tk', 'scaling', scale)
    except Exception:
        pass


def _set_adaptive_geometry(root):
    root.update_idletasks()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    win_w = min(int(sw * 0.92), 1600)
    win_h = min(int(sh * 0.92), 950)

    win_w = max(win_w, 900)
    win_h = max(win_h, 560)

    x = (sw - win_w) // 2
    y = max(0, (sh - win_h) // 2 - 20)   # slightly above centre looks better
    root.geometry(f"{win_w}x{win_h}+{x}+{y}")
    root.minsize(860, 520)


def main():
    root = tk.Tk()
    root.title("Graph Topology Engine Dashboard")

    _apply_dpi_scaling(root)
    _set_adaptive_geometry(root)

    state.algo_color = "#00e5ff"

    
    root.rowconfigure(0, weight=0)   
    root.rowconfigure(1, weight=1)   
    root.columnconfigure(0, weight=16)
    root.columnconfigure(1, weight=73)
    root.columnconfigure(2, weight=11)

    
    top_header_bar = tk.Frame(root, bg="#0e101a", height=55,
                              highlightthickness=1, highlightbackground="#1b1e2e")
    top_header_bar.grid(row=0, column=0, columnspan=3, sticky="ew")
    top_header_bar.grid_propagate(False)   

    app_title_lbl = tk.Label(
        top_header_bar,
        text=" ⚡ GRAPH TRAVERSAL DIAGNOSTIC DASHBOARD",
        font=("Consolas", 15, "bold"),
        fg="#00e5ff", bg="#0e101a"
    )
    app_title_lbl.pack(side="left", padx=15, pady=12)
    state._app_title_lbl = app_title_lbl

    canvas_result = ui_canvas.build_canvas(root)
    canvas = canvas_result["canvas"]

    left_result = ui_left_sidebar.build_left_sidebar(
        root, canvas,
        canvas_result["frame"],
        canvas_result["pan_tip_lbl"]
    )
    right_result = ui_right_sidebar.build_right_sidebar(root)

    
    left_result["handle_btn"].config(
        command=lambda: helpers.toggle_left_drawer(
            left_result["sidebar_canvas"], root,
            left_result["handle_btn"],
            left_result["is_left_drawer_open"]
        )
    )

    state._play_search_btn  = left_result["play_search_btn"]
    state._stats_title      = right_result["stats_title"]
    state._frontier_box     = right_result["frontier_box"]
    state._progress_box     = right_result["progress_box"]

    state.canvas            = canvas
    state.status_label      = right_result["status_label"]
    state._status_label     = right_result["status_label"]
    state.hint_label        = right_result["hint_label"]
    state.progress_label    = right_result["progress_box"]
    state.process_label     = right_result["process_label"]
    state.stats_label       = right_result["stats_label"]
    state.frontier_display  = right_result["frontier_box"]
    state.adj_list_display  = right_result["adj_text_widget"]

    state.buttons = {
        "bfs":        left_result["play_search_btn"],
        "dfs":        left_result["play_search_btn"],
        "vertex":     left_result["v_btn"],
        "edge":       left_result["e_btn"],
        "move":       left_result["m_btn"],
        "delete":     left_result["del_v_btn"],
        "edge_delete":left_result["del_e_btn"],
        "restart":    right_result["restart_btn"],
        "previous":   right_result["prev_btn"],
        "pause":      right_result["pause_btn"],
        "step":       right_result["step_btn"],
    }

    state.update_status  = lambda msg: right_result["status_label"].config(text=msg)
    state.update_hint    = lambda msg: right_result["hint_label"].config(text=msg)
    state.update_process = lambda msg: right_result["process_label"].config(text=msg)

    def set_ui_animation_state(is_running, is_paused=False):
        helpers.set_ui_animation_state(
            is_running, is_paused,
            play_search_btn  = left_result["play_search_btn"],
            v_btn            = left_result["v_btn"],
            e_btn            = left_result["e_btn"],
            m_btn            = left_result["m_btn"],
            del_v_btn        = left_result["del_v_btn"],
            del_e_btn        = left_result["del_e_btn"],
            target_setter_btn= left_result["target_setter_btn"],
            prev_btn         = right_result["prev_btn"],
            step_btn         = right_result["step_btn"],
            pause_btn        = right_result["pause_btn"],
            restart_btn      = right_result["restart_btn"],
        )

    state.register_ui_animation_callback(set_ui_animation_state)
    state.set_ui_animation_state = set_ui_animation_state
    state.update_button_states()
    state.update_adjacency_list_ui()

    canvas.bind("<Button-1>",       lambda e: helpers.filtered_canvas_click(e, canvas))
    canvas.bind("<Motion>",         lambda e: helpers.filtered_mouse_move(e, canvas))
    canvas.bind("<B1-Motion>",      lambda e: helpers.filtered_canvas_drag(e, canvas))
    canvas.bind("<ButtonRelease-1>",lambda e: helpers.filtered_canvas_release(e, canvas))
    canvas.bind("<Button-3>",       graph.start_canvas_pan)
    canvas.bind("<B3-Motion>",      graph.drag_canvas_pan)
    canvas.bind("<MouseWheel>",     graph.handle_mouse_wheel_zoom)

    root.mainloop()


if __name__ == "__main__":
    main()