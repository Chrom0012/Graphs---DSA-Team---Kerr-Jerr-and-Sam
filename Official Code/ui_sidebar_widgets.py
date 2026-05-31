"""
ui_sidebar_widgets.py
Reusable sidebar UI components: ToolTip and CollapsibleCategory.
"""
import tkinter as tk


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.enter)
        widget.bind("<Leave>", self.leave)
        widget.bind("<Destroy>", self.on_destroy)

    def on_destroy(self, e=None):
        self.leave()

    def enter(self, e=None):
        if not self.widget.winfo_exists():
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tk.Label(tw, text=self.text, justify="left", background="#ffffe0",
                 relief="solid", borderwidth=1, font=("Consolas", 9)).pack()

    def leave(self, e=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


class CollapsibleCategory:
    def __init__(self, parent, title, open_by_default=True,
                 title_font=("Consolas", 12, "bold")):
        self.parent = parent
        self.title = title
        self.open = tk.BooleanVar(value=open_by_default)

        self.outer = tk.Frame(parent, bg="#0e101a")
        self.outer.pack(fill="x", padx=0, pady=0)

        self.header = tk.Button(
            self.outer,
            text=f"{'▼' if open_by_default else '▶'} {title}",
            font=title_font,
            bg="#1a1c2e", fg="#00e5ff",
            relief="flat", anchor="w", padx=8, pady=6,
            command=self.toggle
        )
        self.header.pack(fill="x", padx=8, pady=(4, 2))

        self.content = tk.Frame(self.outer, bg="#0e101a")
        if open_by_default:
            self.content.pack(fill="x", padx=8, pady=(0, 8))

    def toggle(self):
        if self.open.get():
            self.content.pack_forget()
            self.open.set(False)
            self.header.config(text=f"▶ {self.title}")
        else:
            self.content.pack(fill="x", padx=8, pady=(0, 8))
            self.open.set(True)
            self.header.config(text=f"▼ {self.title}")
