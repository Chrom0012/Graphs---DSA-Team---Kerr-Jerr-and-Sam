"""
traversal_engine.py
BFS/DFS history builder and canvas visual effects (sparks, edge travel).
"""
import time
import collections
import tkinter as tk
import state


# ── Helpers ──────────────────────────────────────────────────────────────────

def _vid_sort_key(vid):
    try:
        return (0, int(vid), "")
    except (ValueError, TypeError):
        return (1, 0, str(vid))

def _neighbor_key(item):
    return _vid_sort_key(item[0])


def clear_any_active_timer():
    if hasattr(state, "animation_timer_id") and state.animation_timer_id:
        try:
            if state.canvas and state.canvas.winfo_exists():
                state.canvas.after_cancel(state.animation_timer_id)
        except Exception:
            pass
        state.animation_timer_id = None


def _safe_delete(item):
    try:
        if state.canvas and state.canvas.winfo_exists():
            state.canvas.delete(item)
    except Exception:
        pass


def _safe_config(item, **kwargs):
    try:
        if state.canvas and state.canvas.winfo_exists():
            state.canvas.itemconfig(item, **kwargs)
    except Exception:
        pass


# ── Canvas effects ────────────────────────────────────────────────────────────

def trigger_ring_spark(vid):
    if not state.canvas or not state.canvas.winfo_exists() or vid not in state.vertices:
        return

    def step(frame=0):
        if frame > 10:
            return
        if not state.canvas or not state.canvas.winfo_exists() or vid not in state.vertices:
            return
        try:
            cx = state.vertices[vid]["x"]
            cy = state.vertices[vid]["y"]
            r = (25 + frame * 8) * state.zoom_scale_tracker
            theme = getattr(state, "algo_color", "#00e5ff")
            ring = state.canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                            outline=theme, width=3)
            state.canvas.after(30, lambda: [_safe_delete(ring), step(frame + 1)])
        except Exception:
            pass

    step(0)


def find_edge_id_between(u, v):
    for neighbor, eid in state.adj_list.get(u, []):
        if neighbor == v:
            return eid
    for neighbor, eid in state.adj_list.get(v, []):
        if neighbor == u:
            return eid
    return None


def trigger_edge_travel(parent_vid, active_vid, on_arrival=None):
    if not (state.canvas and state.canvas.winfo_exists()
            and parent_vid in state.vertices and active_vid in state.vertices):
        if on_arrival:
            on_arrival()
        return

    steps = 12
    delay = 300 // steps
    theme = getattr(state, "algo_color", "#ffd700")
    edge_id = find_edge_id_between(parent_vid, active_vid)

    if edge_id:
        try:
            glow = max(3, int((state.edge_width + 2) * state.zoom_scale_tracker))
            state.canvas.itemconfig(edge_id, fill=theme, width=glow)
        except Exception:
            pass

    def travel_step(frame=0):
        if frame > steps:
            if edge_id:
                try:
                    if state.canvas and state.canvas.winfo_exists():
                        base = max(1, int(state.edge_width * state.zoom_scale_tracker))
                        state.canvas.after(400,
                            lambda: _safe_config(edge_id, fill="#555588", width=base))
                except Exception:
                    pass
            if on_arrival:
                on_arrival()
            return
        try:
            x1 = state.vertices[parent_vid]["x"]
            y1 = state.vertices[parent_vid]["y"]
            x2 = state.vertices[active_vid]["x"]
            y2 = state.vertices[active_vid]["y"]
            t = frame / steps
            cx = x1 + (x2 - x1) * t
            cy = y1 + (y2 - y1) * t
            r = 8 * state.zoom_scale_tracker
            spark = state.canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                             fill=theme, outline="#ffffff", width=2)
            state.canvas.after(delay,
                               lambda: [_safe_delete(spark), travel_step(frame + 1)])
        except Exception:
            if on_arrival:
                on_arrival()

    travel_step(0)


# ── BFS / DFS history builder ────────────────────────────────────────────────

def _make_step(visited, frontier, active, parent, status, structure):
    return {
        "visited":   list(visited),
        "frontier":  list(frontier),
        "active":    active,
        "parent":    parent,
        "status":    status,
        "structure": structure,
    }


def build_bfs_history(root_vid):
    adj = state.adj_list
    history, visited_order, local_visited = [], [], set()
    parent_map = {root_vid: None}
    queue = collections.deque([root_vid])
    local_visited.add(root_vid)
    history.append(_make_step(visited_order, queue, None, None,
                              "Initialized BFS Queue structure.", "queue"))
    while queue:
        curr = queue.popleft()
        visited_order.append(curr)
        history.append(_make_step(visited_order, queue, curr,
                                  parent_map.get(curr),
                                  f"BFS visiting node {curr}.", "queue"))
        if state.target_vertex is not None and str(curr) == str(state.target_vertex):
            history.append(_make_step(visited_order, queue, curr,
                                      parent_map.get(curr),
                                      f"🎯 Target node {curr} intercepted! Search complete.",
                                      "queue"))
            break
        for neighbor, _ in sorted(adj.get(curr, []), key=_neighbor_key):
            if neighbor not in local_visited:
                local_visited.add(neighbor)
                parent_map[neighbor] = curr
                queue.append(neighbor)
                history.append(_make_step(visited_order, queue, curr, curr,
                                          f"Discovered adjacent node {neighbor}.",
                                          "queue"))
    history.append(_make_step(visited_order, [], None, None,
                              "Traversal completed.", "queue"))
    return history


def build_dfs_history(root_vid):
    adj = state.adj_list
    history, visited_order, local_visited = [], [], set()
    parent_map = {root_vid: None}
    stack = [root_vid]
    history.append(_make_step(visited_order, stack, None, None,
                              "Initialized DFS Stack structure.", "stack"))
    while stack:
        curr = stack.pop()
        if curr in local_visited:
            continue
        local_visited.add(curr)
        visited_order.append(curr)
        history.append(_make_step(visited_order, stack, curr,
                                  parent_map.get(curr),
                                  f"DFS expanding node {curr}.", "stack"))
        if state.target_vertex is not None and str(curr) == str(state.target_vertex):
            history.append(_make_step(visited_order, stack, curr,
                                      parent_map.get(curr),
                                      f"🎯 Target node {curr} intercepted! Search complete.",
                                      "stack"))
            break
        for neighbor, _ in sorted(adj.get(curr, []), key=_neighbor_key, reverse=True):
            if neighbor not in local_visited:
                stack.append(neighbor)
                if neighbor not in parent_map:
                    parent_map[neighbor] = curr
                history.append(_make_step(visited_order, stack, curr, curr,
                                          f"Pushed adjacent node {neighbor} to stack.",
                                          "stack"))
    history.append(_make_step(visited_order, [], None, None,
                              "Traversal completed.", "stack"))
    return history
