import state

def animate_vertex_bounce(vid, cx, cy, frame=0):
    if not state.canvas or not state.canvas.winfo_exists():
        return
    base_r = state.vertex_radius
    ratio = base_r / 22.0
    raw_seq = [4, 11, 19, 27, 24, 21, 22]
    radius_sequence = [max(1, round(v * ratio)) for v in raw_seq]
    radius_sequence[-1] = base_r

    if frame >= len(radius_sequence) or vid not in state.vertices:
        return
    r = radius_sequence[frame] * state.zoom_scale_tracker
    try:
        state.canvas.coords(
            state.vertices[vid]["circle"],
            cx - r, cy - r, cx + r, cy + r
        )
    except:
        return
    state.canvas.after(
        20,
        lambda: animate_vertex_bounce(vid, cx, cy, frame + 1)
    )

def animate_edge_growth(edge_id, sx, sy, ex, ey, frame=0, total_frames=8):
    if not state.canvas or not state.canvas.winfo_exists():
        return
    if frame > total_frames:
        return
    pct = frame / total_frames
    cx = sx + (ex - sx) * pct
    cy = sy + (ey - sy) * pct
    try:
        state.canvas.coords(edge_id, sx, sy, cx, cy)
    except:
        return
    state.canvas.after(
        20,
        lambda: animate_edge_growth(edge_id, sx, sy, ex, ey, frame + 1, total_frames)
    )

def trigger_radar_pulse(cx, cy, max_r=75, current_r=22, wave_color=None):
    if not state.canvas or not state.canvas.winfo_exists():
        return
    if wave_color is None:
        wave_color = getattr(state, "algo_color", "#ffd700")
    if current_r >= max_r:
        return
    try:
        pulse_id = state.canvas.create_oval(
            cx - current_r, cy - current_r,
            cx + current_r, cy + current_r,
            outline=wave_color, width=2
        )
        state.canvas.tag_lower(pulse_id)
        state.canvas.after(45, lambda: state.canvas.delete(pulse_id))
        state.canvas.after(
            25,
            lambda: trigger_radar_pulse(cx, cy, max_r, current_r + 6, wave_color)
        )
    except:
        pass

def fire_traveling_photon_pulse(sx, sy, ex, ey, color, completion_callback,
                                 frame=0, total_frames=12):
    if not state.canvas or not state.canvas.winfo_exists():
        return
    if frame > total_frames:
        completion_callback()
        return
    pct = frame / total_frames
    cx = sx + (ex - sx) * pct
    cy = sy + (ey - sy) * pct
    dot_r = 6 * state.zoom_scale_tracker
    try:
        pulse_dot = state.canvas.create_oval(
            cx - dot_r, cy - dot_r,
            cx + dot_r, cy + dot_r,
            fill=color, outline=""
        )
        state.canvas.after(
            20,
            lambda: [
                state.canvas.delete(pulse_dot),
                fire_traveling_photon_pulse(sx, sy, ex, ey, color,
                                            completion_callback, frame + 1, total_frames)
            ]
        )
    except:
        pass
