import tkinter as tk

Mode = "Node"
mark = 0
lastx = 0
lasty = 0

def main():
    global Mode, mark, lastx, lasty
    
    Root = tk.Tk()
    Root.title("Example lang this")
    Root.geometry("700x500")

    def createNodeAtClick(location):
        global mark, lastx, lasty, Mode
        if Mode == "Node":
            Canvas.create_oval(location.x - 25, location.y - 25, location.x + 25, location.y + 25, fill="green")
            Canvas.create_text(location.x, location.y, text=f"{location.x}, {location.y}", font=("Arial", 10, "bold"), fill="white")
            mark = 0
            lastx = location.x
            lasty = location.y
        else:
            HighlightCreateEdge(location)
            """
            Canvas.create_oval(location.x - 25, location.y - 25, location.x + 25, location.y + 25, fill="green")
            Canvas.create_text(location.x, location.y, text=f"{location.x}, {location.y}", font=("Arial", 10, "bold"), fill="white")
            if mark != 0:
                line = Canvas.create_line(lastx, lasty, location.x, location.y, fill="black", width=2)
                Canvas.tag_lower(line)
            lastx = location.x
            lasty = location.y
            mark = 1
            """

    def ResetTheNodeClicked():
        global mark
        Canvas.delete("all")
        mark = 0

    def AddNode():
        global Mode
        Mode = "Node"
        status.config(text="Status: Adding Nodes")

    def AddEdge():
        global Mode
        Mode = "Edge"
        status.config(text="Status: Adding Edges")
    
    def hoverHighlightNode(event):
        x, y = event.x, event.y
        items = Canvas.find_overlapping(x-25, y-25, x+25, y+25)
        for item in items:
            if Canvas.type(item) == "oval":
                Canvas.itemconfig(item, fill="yellow")
            else:
                Canvas.itemconfig(item, fill="green")
        for item in Canvas.find_all():
            if item not in items and Canvas.type(item) == "oval":
                Canvas.itemconfig(item, fill="green")
    
    def HighlightCreateEdge(event):
        global lastx, lasty, mark
        x, y = event.x, event.y
        items = Canvas.find_overlapping(x-25, y-25, x+25, y+25)
        for item in items:
            if Canvas.type(item) == "oval":
                Canvas.itemconfig(item, fill="yellow")
                if mark != 0:
                    line = Canvas.create_line(lastx, lasty, x, y, fill="black", width=2)
                    Canvas.tag_lower(line)
                lastx = x
                lasty = y
                mark = 1
            else:
                Canvas.itemconfig(item, fill="green")
        

    sidebar = tk.Frame(Root, width=200, bg="lightgray", relief="sunken", borderwidth=2)
    sidebar.grid(row=0, column=0, sticky="ns")

    Canvas = tk.Canvas(Root, height=500, width=700, bg="white")
    Canvas.grid(row=0, column=1, sticky="nsew")

    button_node = tk.Button(sidebar, text="Add Node", command=AddNode)
    button_node.pack(pady=10)

    button_edge = tk.Button(sidebar, text="Add Edge", command=AddEdge)
    button_edge.pack(pady=10)

    button_clear = tk.Button(sidebar, text="Reset", command=ResetTheNodeClicked)
    button_clear.pack(pady=10)

    status = tk.Label(sidebar, text="Status: Adding Nodes", bg="lightgray")
    status.pack(side="bottom", pady=10)

    Canvas.bind("<Button-1>", createNodeAtClick)
    Canvas.bind("<Motion>", lambda event: hoverHighlightNode(event))
    Canvas.bind("<Button-3>", lambda event: HighlightCreateEdge(event))

    return Root