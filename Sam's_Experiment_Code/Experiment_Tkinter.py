import tkinter as tk 

Root = tk.Tk()
Root.title("Example lang this")
Root.geometry("500x500")

Canvas = tk.Canvas(Root, height = 500, width = 500)
Canvas.pack(pady=20)
Canvas.create_text(250,20, text = "Graph Example", font = ("Arial", 16, "bold"))
Canvas.create_oval(50, 30, 150, 140, fill = "red")
Canvas.create_text(100, 85, text = "Node A", font = ("Arial", 12, "bold"))
Canvas.create_oval(200, 30, 300, 140, fill = "blue")
Canvas.create_text(250, 85, text = "Node B", font = ("Arial", 12, "bold"), fill = "white")
Canvas.create_line(150, 85, 200, 85, fill = "black", width = 2)
mark = 0
lastx = 0
lasty = 0

def createNodeAtClick(location):
    global mark, lastx, lasty
    if mark == 0:
        lastx = location.x
        lasty = location.y
        print(location.x, location.y)
        Canvas.create_oval(location.x - 25, location.y - 25, location.x + 25, location.y + 25, fill = "green")
        Canvas.create_text(location.x, location.y, text = f"{location.x}, {location.y}", font = ("Arial", 10, "bold"), fill = "white")
        mark = 1
    else:
        print(location.x, location.y)
        Canvas.create_oval(location.x - 25, location.y - 25, location.x + 25, location.y + 25, fill = "green")
        Canvas.create_text(location.x, location.y, text = f"{location.x}, {location.y}", font = ("Arial", 10, "bold"), fill = "white")
        Canvas.create_line(lastx, lasty, location.x, location.y, fill= "black", width = 2)
        lastx = location.x
        lasty = location.y



Canvas.bind("<Button-1>", createNodeAtClick)

Root.mainloop()