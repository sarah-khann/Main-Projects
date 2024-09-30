from spine import *
from circles import *

import tkinter as tk

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs.pop("end") - kwargs["start"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle_arc = _create_circle_arc

class SketchTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Sketch Tool")

        #  here da canvas 
        self.canvas = tk.Canvas(root, bg='white', width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # points display 
        self.text_output = tk.Text(root, height=10, width=80)
        self.text_output.pack(side=tk.BOTTOM, fill=tk.X)

        self.drawing = False
        self.last_x, self.last_y = None, None
        self.points = []  # list storing points 

        
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def start_drawing(self, event):
        # begin drawing when button pressed 
        self.canvas.delete("all")
        self.drawing = True
        self.last_x, self.last_y = event.x, event.y
        self.points.clear()  

    def draw(self, event):
        if self.drawing:
            if self.last_x is not None and self.last_y is not None:
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill='black', width=2)
                self.points.append(Point(self.last_x, self.last_y))
            self.last_x, self.last_y = event.x, event.y
            self.points.append(Point(self.last_x, self.last_y))  

    def stop_drawing(self, event):
        self.drawing = False
        self.last_x, self.last_y = None, None
        self.prune(5)
        self.display_points()
        data = method_one(self.points)
        clean_circles(data)
        self.gen_draw(data)
        self.highlight()


    def display_points(self):
        self.text_output.delete('1.0', tk.END)
        self.text_output.insert(tk.END, "Points on the drawn line:\n")
        for point in self.points:
            self.text_output.insert(tk.END, f"{point.x} {point.y}\n")

    def prune(self, n: int) -> None:
        """prunes off every n element"""
        temp = []
        for i in range(len(self.points)):
            if(i % n == 0):
                temp.append(self.points[i])
        
        self.points = temp

    def highlight(self) -> None:
        """highlights the points cuh"""
        for i in range(len(self.points)):
            self.canvas.create_oval(self.points[i].x, self.points[i].y,self.points[i].x, self.points[i].y, fill = "hot pink", width = 4, outline="hot pink")
        
    def gen_draw(self, arr_circ: list[Circle]):
        """draws everything given circles"""
        for c in arr_circ:
            self.canvas.create_circle(c.p.x, c.p.y, c.r, outline="#ff8080", width=1)


root = tk.Tk()
sketch_tool = SketchTool(root)

root.mainloop()
