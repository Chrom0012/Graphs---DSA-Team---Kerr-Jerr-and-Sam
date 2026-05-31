"""
Part 2 of graph_interaction.py: Vertex ID dialog.
"""
import tkinter as tk
from tkinter import messagebox
import state
import animation
import traversal
from graph_core import (
    get_contrast_color, edge_exists, calculate_edge_endpoints,
    redraw_graph, highlight_vertex, unhighlight_vertex,
    select_vertex, deselect_vertex
)


# ── Vertex ID dialog ─────────────────────────────────────────────────────────

def ask_vertex_details(parent_win):
    result = {"id": None, "data": ""}
    dialog = tk.Toplevel(parent_win)
    dialog.title("Vertex Node Setup")
    dialog.geometry("380x240")
    dialog.resizable(False, False)
    dialog.configure(bg="#1a1c2e")
    dialog.transient(parent_win)
    dialog.grab_set()

    dialog.update_idletasks()
    px = parent_win.winfo_rootx() + (parent_win.winfo_width() // 2) - 190
    py = parent_win.winfo_rooty() + (parent_win.winfo_height() // 2) - 120
    dialog.geometry(f"+{px}+{py}")

    tk.Label(dialog, text="Naming Mode:", fg="#00e5ff", bg="#1a1c2e",
             font=("Consolas", 10, "bold")).pack(pady=(12, 2))
    mode_var = tk.StringVar(value=state.vertex_naming_mode)
    mode_frame = tk.Frame(dialog, bg="#1a1c2e")
    mode_frame.pack(pady=2)
    for m, lbl in [("integer", "Integer"), ("letter", "Letter"), ("custom", "Custom")]:
        tk.Radiobutton(mode_frame, text=lbl, variable=mode_var, value=m,
                       bg="#1a1c2e", fg="white", selectcolor="#2e3456",
                       font=("Consolas", 10)).pack(side="left", padx=5)

    id_frame = tk.Frame(dialog, bg="#1a1c2e")
    tk.Label(id_frame, text="Vertex ID (Custom mode only):", fg="#ffffff", bg="#1a1c2e",
             font=("Consolas", 10)).pack(pady=(8, 2))
    id_entry = tk.Entry(id_frame, bg="#2e314d", fg="white", insertbackground="white",
                        font=("Consolas", 10), justify="center", width=24)
    id_entry.pack(pady=2)

    data_frame = tk.Frame(dialog, bg="#1a1c2e")
    tk.Label(data_frame, text="Custom Data (Optional):", fg="#ffffff", bg="#1a1c2e",
             font=("Consolas", 10)).pack(pady=(8, 2))
    data_entry = tk.Entry(data_frame, bg="#2e314d", fg="white", insertbackground="white",
                          font=("Consolas", 10), justify="center", width=24)
    data_entry.pack(pady=2)
    data_frame.pack(pady=2)

    def update_id_visibility(*_):
        if mode_var.get() == "custom":
            id_frame.pack(pady=2, before=data_frame)
        else:
            id_frame.pack_forget()
    mode_var.trace_add("write", update_id_visibility)
    update_id_visibility()

    def on_confirm(event=None):
        m = mode_var.get()
        if m == "integer":
            vid = str(state.next_auto_index); state.next_auto_index += 1
        elif m == "letter":
            n, res = state.next_auto_index, ""
            while n >= 0:
                res = chr(n % 26 + 65) + res; n = n // 26 - 1
            vid = res; state.next_auto_index += 1
        else:
            vid = id_entry.get().strip()
            if not vid:
                messagebox.showwarning("Validation Error", "Vertex ID cannot be empty.", parent=dialog)
                return
        custom = data_entry.get().strip()
        if vid in state.vertices:
            messagebox.showwarning("Duplicate Identity", f"Vertex '{vid}' already exists.", parent=dialog)
            return
        result["id"] = vid; result["data"] = custom
        dialog.destroy()

    dialog.bind("<Return>", on_confirm)
    tk.Button(dialog, text="Generate Node", bg="#00e5ff", fg="black",
              activebackground="#00b2cc", font=("Consolas", 10, "bold"),
              width=15, command=on_confirm, bd=0).pack(pady=15)
    parent_win.wait_window(dialog)
    return result["id"], result["data"]