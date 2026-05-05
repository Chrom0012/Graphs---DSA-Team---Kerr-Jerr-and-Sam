import tkinter as tk 

Root = tk.Tk()
Root.title("Example lang this")
Root.geometry("700x500")

mark = 0
lastx = 0
lasty = 0

def createNodeAtClick(location):
    global mark, lastx, lasty, Mode
    if Mode == "Node":
        print(location.x, location.y)
        Canvas.create_oval(location.x - 25, location.y - 25, location.x + 25, location.y + 25, fill = "green")
        Canvas.create_text(location.x, location.y, text = f"{location.x}, {location.y}", font = ("Arial", 10, "bold"), fill = "white")
        mark = 0
    else:
        print(location.x, location.y)
        Canvas.create_oval(location.x - 25, location.y - 25, location.x + 25, location.y + 25, fill = "green")
        Canvas.create_text(location.x, location.y, text = f"{location.x}, {location.y}", font = ("Arial", 10, "bold"), fill = "white")
        if mark != 0:
            line = Canvas.create_line(lastx, lasty, location.x, location.y, fill= "black", width = 2)
            Canvas.tag_lower(line)
        lastx = location.x
        lasty = location.y
        mark = 1
def ResetTheNodeClicked():
    global mark
    Canvas.delete("all")
    mark = 0
def AddNode():
    global Mode
    Mode = "Node"
    status.config(text = "Status: Adding Nodes")
def AddEdge():
    global Mode
    Mode = "Edge"
    status.config(text = "Status: Adding Edges")
sidebar = tk.Frame(Root, width = 200, bg = "lightgray", relief = "sunken", borderwidth = 2)
sidebar.grid(row = 0, column = 0, sticky = "ns")

button_clear = tk.Button(sidebar, text = "Reset", command = ResetTheNodeClicked)
button_clear.pack(pady = 10)
Canvas = tk.Canvas(Root, height = 500, width = 700)
Canvas.grid(row = 0, column = 1, sticky = "nsew")
button_node = tk.Button(sidebar, text = "Add Node", command = AddNode)
button_node.pack(pady = 10)
button_edge = tk.Button(sidebar, text = "Add Edge", command = AddEdge)
button_edge.pack(pady = 10)
status = tk.Label(sidebar, text = "Status: Adding Nodes", bg = "lightgray")
status.pack(side = "bottom", pady = 10)
Mode = "Node"




Canvas.bind("<Button-1>", createNodeAtClick)

Root.mainloop()
