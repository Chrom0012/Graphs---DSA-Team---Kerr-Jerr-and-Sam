import tkinter as tk 

Root = tk.Tk()
Root.title("Example lang this")
Root.geometry("500x500")

Canvas = tk.Canvas(Root, height = 500, width = 500)
Canvas.pack(pady=20)

Canvas.create_oval(50, 30, 150, 140, fill = "red")
Canvas.create_text(100, 85, text = "Node A", font = ("Arial", 12, "bold"))
Root.mainloop()