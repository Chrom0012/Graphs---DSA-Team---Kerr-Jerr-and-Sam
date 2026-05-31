import tkinter as tk
import state
import ui_helpers as helpers


def build_canvas(root):
    center_workspace_frame = tk.Frame(root, bg=state.canvas_bg_color)
    center_workspace_frame.grid(row=1, column=1, sticky="nsew")

    canvas = tk.Canvas(
        center_workspace_frame,
        bg=state.canvas_bg_color,
        highlightthickness=0,
        scrollregion=(-4000, -4000, 4000, 4000)
    )
    canvas.pack(fill="both", expand=True)

    workspace_controls = tk.Frame(canvas, bg="#0e101a",
                                  highlightthickness=1, highlightbackground="#1b1e2e")
    workspace_controls.place(x=15, y=15, width=190, height=32)

    tk.Button(
        workspace_controls, text="Zoom [ + ]",
        font=("Consolas", 9, "bold"), bg="#1a1c2e", fg="white", relief="flat",
        command=lambda: helpers.safe_zoom_in(canvas)
    ).pack(side="left", fill="both", expand=True, padx=1, pady=1)

    tk.Button(
        workspace_controls, text="Zoom [ - ]",
        font=("Consolas", 9, "bold"), bg="#1a1c2e", fg="white", relief="flat",
        command=lambda: helpers.safe_zoom_out(canvas)
    ).pack(side="left", fill="both", expand=True, padx=1, pady=1)

    pan_tip_lbl = tk.Label(
        center_workspace_frame,
        text="🖱 Right-Click Drag Canvas to Pan  |  Scroll to Zoom",
        font=("Consolas", 10), fg="#8899cc", bg=state.canvas_bg_color
    )
    pan_tip_lbl.place(x=15, y=54)

    return {
        "frame": center_workspace_frame,
        "canvas": canvas,
        "pan_tip_lbl": pan_tip_lbl,
    }
