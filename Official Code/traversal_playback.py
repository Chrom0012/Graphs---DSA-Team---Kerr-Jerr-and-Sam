"""
traversal_playback.py
Step rendering, animation loop, pause / step-forward / step-backward / restart.
"""
import time
import tkinter as tk
import state
from traversal_engine import (
    clear_any_active_timer, trigger_ring_spark, trigger_edge_travel,
    build_bfs_history, build_dfs_history,
)


# ── Mode starters ─────────────────────────────────────────────────────────────

def start_bfs_mode():
    clear_any_active_timer()
    state.mode = "pick_bfs_root"
    state.update_status("Status: Pick BFS Root")
    state.update_hint("💡 Click on any node on the canvas to set it as the BFS starting root.")


def start_dfs_mode():
    clear_any_active_timer()
    state.mode = "pick_dfs_root"
    state.update_status("Status: Pick DFS Root")
    state.update_hint("💡 Click on any node on the canvas to set it as the DFS starting root.")


# ── Visual reset ──────────────────────────────────────────────────────────────

def reset_visual_state():
    clear_any_active_timer()
    state.traversal_history = []
    state.current_step_index = 0
    state.is_running = False
    state.is_paused = False
    state._traversal_start_time = None

    for attr in ("frontier_display", "progress_label"):
        w = getattr(state, attr, None)
        if w and w.winfo_exists():
            try:
                w.config(state="normal")
                w.delete("1.0", tk.END)
                w.config(state="disabled")
            except Exception:
                pass

    state.update_stats_display(0, 0, 0)
    state.update_adjacency_list_ui(highlight=None)

    if state.canvas and state.canvas.winfo_exists():
        for vid, node in state.vertices.items():
            if "circle" in node:
                try:
                    col = node.get("color", state.vertex_fill_color)
                    state.canvas.itemconfig(
                        node["circle"], fill=col, outline="#333355",
                        width=max(1, int(2 * state.zoom_scale_tracker))
                    )
                except Exception:
                    pass


# ── Search entry points ───────────────────────────────────────────────────────

def initialize_search_sequence(root_vid, search_type):
    clear_any_active_timer()
    state._traversal_start_time = time.time()

    if search_type == "bfs":
        state.traversal_history = build_bfs_history(root_vid)
    else:
        state.traversal_history = build_dfs_history(root_vid)

    state.current_step_index = 0
    state.is_running = True
    state.is_paused = False
    state.mode = "animate"
    state.set_ui_animation_state(True, False)

    apply_step_state(0, trigger_effects=True, update_stats=False)
    run_animation_loop()


def run_bfs(root_vid):
    initialize_search_sequence(root_vid, "bfs")


def run_dfs(root_vid):
    initialize_search_sequence(root_vid, "dfs")


# ── Animation loop ────────────────────────────────────────────────────────────

def run_animation_loop():
    if not state.is_running or state.is_paused:
        return
    clear_any_active_timer()
    if state.current_step_index < len(state.traversal_history) - 1:
        state.current_step_index += 1
        apply_step_state(state.current_step_index, trigger_effects=True, update_stats=True)
        delay = getattr(state, "animation_speed", 650)
        # FIX: Ensure canvas still exists before scheduling next step
        try:
            if state.canvas and state.canvas.winfo_exists():
                state.animation_timer_id = state.canvas.after(delay, run_animation_loop)
        except Exception:
            # If canvas is gone, stop the animation cleanly
            state.is_running = False
    else:
        _finish_animation()


def _finish_animation():
    state.is_running = False
    last = state.traversal_history[-1]
    visited = len(last["visited"])
    total = len(state.vertices)
    if visited < total:
        state.update_status(
            f"Status: Traversal finished – {visited}/{total} vertices visited (graph is disconnected).")
        state.update_hint(f"⚠️ Only {visited} out of {total} nodes were reachable from root.")
    else:
        state.update_status("Status: Traversal Completed Successfully!")
    state.set_ui_animation_state(False)
    if state._traversal_start_time:
        elapsed = int((time.time() - state._traversal_start_time) * 1000)
        state.update_stats_display(elapsed, visited, len(state.traversal_history) - 1)
    import ui_helpers as helpers
    helpers.auto_open_left_drawer()


# ── Step renderer ─────────────────────────────────────────────────────────────

def apply_step_state(index, trigger_effects=False, update_stats=True):
    if not state.traversal_history or index >= len(state.traversal_history):
        return
    if not state.canvas or not state.canvas.winfo_exists():
        return

    step = state.traversal_history[index]
    state.update_process(f"Processing Step: {index + 1} / {len(state.traversal_history)}")
    state.update_hint(step["status"])

    if update_stats and state._traversal_start_time:
        elapsed = int((time.time() - state._traversal_start_time) * 1000)
        state.update_stats_display(elapsed, len(step["visited"]), index + 1)

    structure = step.get("structure", "queue")
    state.update_live_frontier_ui(step["frontier"],
                                  "QUEUE" if structure == "queue" else "STACK")

    pl = getattr(state, "progress_label", None)
    if pl and pl.winfo_exists():
        try:
            pl.config(state="normal")
            pl.delete("1.0", tk.END)
            roadmap = " ➔ ".join(map(str, step["visited"]))
            pl.insert("1.0", roadmap if roadmap else "[ None ]")
            pl.config(state="disabled")
        except Exception:
            pass

    state.update_adjacency_list_ui(highlight=step["active"])
    _paint_vertices(step)

    if trigger_effects and step["active"] is not None:
        active_vid = step["active"]
        parent_vid = step.get("parent")
        if active_vid in state.vertices:
            if parent_vid and parent_vid in state.vertices:
                trigger_edge_travel(parent_vid, active_vid,
                                    on_arrival=lambda: trigger_ring_spark(active_vid))
            else:
                trigger_ring_spark(active_vid)


def _paint_vertices(step):
    active_color = getattr(state, "algo_color", "#ffd700")
    visited_fill = "#eccc68" if active_color == "#ffd700" else "#006680"
    visited_line = "#ff7f50" if active_color == "#ffd700" else "#00b8d4"

    for vid, node in state.vertices.items():
        if "circle" not in node:
            continue
        try:
            circ = node["circle"]
            if vid == step["active"]:
                state.canvas.itemconfig(circ, fill=active_color, outline="#ffffff", width=3)
            elif vid in step["visited"]:
                state.canvas.itemconfig(circ, fill=visited_fill, outline=visited_line, width=2)
            elif vid in step["frontier"]:
                state.canvas.itemconfig(circ, fill="#2f3542", outline="#00e5ff", width=2)
            else:
                col = node.get("color", state.vertex_fill_color)
                state.canvas.itemconfig(circ, fill=col, outline="#333355",
                                        width=max(1, int(2 * state.zoom_scale_tracker)))
        except Exception:
            pass


# ── Playback controls ─────────────────────────────────────────────────────────

def toggle_pause():
    import ui_helpers as helpers
    if not state.is_running:
        return
    if not state.is_paused:
        clear_any_active_timer()
        state.is_paused = True
        state.update_status("Status: Paused")
        try:
            state.buttons["pause"].config(text="▶")
        except Exception:
            pass
        state.set_ui_animation_state(True, True)
        helpers.auto_open_left_drawer()
    else:
        state.is_paused = False
        state.update_status("Status: Running Traversal...")
        try:
            state.buttons["pause"].config(text="⏸")
        except Exception:
            pass
        state.set_ui_animation_state(True, False)
        helpers.auto_close_left_drawer()
        run_animation_loop()


def step_backward():
    clear_any_active_timer()
    if state.current_step_index > 0:
        state.current_step_index -= 1
        apply_step_state(state.current_step_index, trigger_effects=False, update_stats=True)


def step_forward():
    clear_any_active_timer()
    if state.current_step_index < len(state.traversal_history) - 1:
        state.current_step_index += 1
        apply_step_state(state.current_step_index, trigger_effects=True, update_stats=True)


def restart_traversal():
    clear_any_active_timer()
    if not state.traversal_history:
        return
    state.current_step_index = 0
    state.is_running = True
    state.is_paused = True
    state._traversal_start_time = time.time()
    try:
        state.buttons["pause"].config(text="▶")
    except Exception:
        pass
    state.set_ui_animation_state(True, True)
    apply_step_state(0, trigger_effects=True, update_stats=False)
    import ui_helpers as helpers
    helpers.auto_open_left_drawer()