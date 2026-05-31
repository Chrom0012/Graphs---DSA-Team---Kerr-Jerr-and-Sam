"""
ui_controls.py
Vertex-size, edge-width, animation speed, target-vertex, and preview-popup helpers.
"""
import state
import graph


# ── Size-mode toggle buttons ──────────────────────────────────────────────────

def update_size_mode_buttons(size_mode_var, r_mode_btn, d_mode_btn, size_entry_label):
    if size_mode_var.get() == "radius":
        r_mode_btn.config(bg="#00e5ff", fg="black")
        d_mode_btn.config(bg="#1a1c2e", fg="white")
        size_entry_label.config(text="R:")
    else:
        r_mode_btn.config(bg="#1a1c2e", fg="white")
        d_mode_btn.config(bg="#00e5ff", fg="black")
        size_entry_label.config(text="D:")


def switch_to_radius(size_mode_var, size_entry, r_mode_btn, d_mode_btn, size_entry_label):
    if size_mode_var.get() != "radius":
        try:
            cur = int(size_entry.get().strip())
            size_entry.delete(0, "end")
            size_entry.insert(0, str(max(5, cur // 2)))
        except Exception:
            size_entry.delete(0, "end")
            size_entry.insert(0, str(state.vertex_radius))
    size_mode_var.set("radius")
    update_size_mode_buttons(size_mode_var, r_mode_btn, d_mode_btn, size_entry_label)


def switch_to_diameter(size_mode_var, size_entry, r_mode_btn, d_mode_btn, size_entry_label):
    if size_mode_var.get() != "diameter":
        try:
            cur = int(size_entry.get().strip())
            size_entry.delete(0, "end")
            size_entry.insert(0, str(cur * 2))
        except Exception:
            size_entry.delete(0, "end")
            size_entry.insert(0, str(state.vertex_radius * 2))
    size_mode_var.set("diameter")
    update_size_mode_buttons(size_mode_var, r_mode_btn, d_mode_btn, size_entry_label)


def on_slider_change(val, size_mode_var, size_entry, slider_syncing):
    if slider_syncing[0]:
        return
    slider_syncing[0] = True
    r_val = int(val)
    display = r_val if size_mode_var.get() == "radius" else r_val * 2
    size_entry.delete(0, "end")
    size_entry.insert(0, str(display))
    slider_syncing[0] = False


# ── Size preview popup ────────────────────────────────────────────────────────

def show_size_preview_popup(canvas, popup_items, popup_cancel_id):
    if not canvas or not canvas.winfo_exists():
        return
    if popup_cancel_id[0]:
        try:
            canvas.after_cancel(popup_cancel_id[0])
        except Exception:
            pass
    for item in popup_items:
        try:
            canvas.delete(item)
        except Exception:
            pass
    popup_items.clear()

    cw = canvas.winfo_width() or 800
    ch = canvas.winfo_height() or 500
    cx = canvas.canvasx(cw - 140)
    cy = canvas.canvasy(80)
    r_px = state.vertex_radius
    pad = 14
    box_r = r_px + pad

    bg = canvas.create_rectangle(cx - box_r - 60, cy - box_r - 10,
                                  cx + box_r + 10, cy + box_r + 10,
                                  fill="#f0f4ff", outline="#3355aa", width=2)
    circle = canvas.create_oval(cx - r_px, cy - r_px, cx + r_px, cy + r_px,
                                 fill=state.vertex_fill_color,
                                 outline="#3355aa", width=2)
    contrast = graph.get_contrast_color(state.vertex_fill_color)
    txt = canvas.create_text(cx, cy, text="A", fill=contrast,
                              font=("Consolas", max(6, int(r_px * 0.5)), "bold"))
    info = canvas.create_text(cx - r_px - 8, cy,
                               text=f"  R = {r_px}px\n  D = {r_px * 2}px",
                               fill="#1a2a6a",
                               font=("Consolas", 9, "bold"), anchor="e")
    popup_items.extend([bg, circle, txt, info])

    def dismiss():
        for item in popup_items:
            try:
                canvas.delete(item)
            except Exception:
                pass
        popup_items.clear()
    popup_cancel_id[0] = canvas.after(2200, dismiss)


# ── Apply vertex size ─────────────────────────────────────────────────────────

def apply_vertex_size(size_entry, size_mode_var, size_slider,
                      slider_syncing, canvas, popup_items,
                      popup_cancel_id, focus_widget):
    try:
        val = int(size_entry.get().strip())
        radius = max(5, val // 2) if size_mode_var.get() == "diameter" else max(5, val)
        radius = min(radius, 80)
        state.vertex_radius = radius
        slider_syncing[0] = True
        size_slider.set(radius)
        slider_syncing[0] = False
        graph.redraw_graph()
    except Exception:
        state.vertex_radius = 22
        size_entry.delete(0, "end")
        size_entry.insert(0, "22")
        graph.redraw_graph()
    focus_widget.focus_set()
    show_size_preview_popup(canvas, popup_items, popup_cancel_id)


# ── Edge width ────────────────────────────────────────────────────────────────

def on_edge_width_slider(val, edge_width_entry, edge_width_syncing):
    if edge_width_syncing[0]:
        return
    edge_width_syncing[0] = True
    edge_width_entry.delete(0, "end")
    edge_width_entry.insert(0, str(int(val)))
    edge_width_syncing[0] = False


def apply_edge_width(edge_width_entry, edge_width_slider,
                     edge_width_syncing, focus_widget):
    try:
        val = int(edge_width_entry.get().strip())
        state.edge_width = max(1, min(10, val))
        edge_width_syncing[0] = True
        edge_width_slider.set(state.edge_width)
        edge_width_syncing[0] = False
        if state.graph_is_not_empty():
            graph.redraw_graph()
    except Exception:
        state.edge_width = 2
        edge_width_entry.delete(0, "end")
        edge_width_entry.insert(0, "2")
    focus_widget.focus_set()


# ── Target vertex ─────────────────────────────────────────────────────────────

def push_target_assignment(target_entry, focus_widget):
    raw = target_entry.get().strip()
    if raw == "":
        state.target_vertex = None
        state.update_hint("💡 Target filter cleared.")
    else:
        state.target_vertex = raw
        state.update_hint(f"🎯 Target Locked: '{raw}'")
    focus_widget.focus_set()


# ── Animation speed ───────────────────────────────────────────────────────────

def apply_speed(speed_entry, focus_widget):
    try:
        val = int(speed_entry.get())
        state.set_animation_speed(max(50, val))
    except Exception:
        state.set_animation_speed(650)
    focus_widget.focus_set()
