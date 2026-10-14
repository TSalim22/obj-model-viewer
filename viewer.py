import tkinter as tk
from tkinter import ttk,filedialog,messagebox
from pathlib import Path
from model import load_obj,normalize,project


class Viewer:
    def __init__(self,root):
        self.root = root
        self.vertices,self.edges = [],[]
        root.title('OBJ Wireframe Viewer')
        root.geometry('920x750')
        toolbar = ttk.Frame(root,padding=12)
        toolbar.pack(fill='x')
        ttk.Button(toolbar,text='Open OBJ',command=self.open).pack(side='left')
        ttk.Button(toolbar,text='Reset view',command=self.reset).pack(side='left',padx=8)
        ttk.Label(toolbar,text='Drag to rotate · Scroll to zoom · OBJ polygon meshes only').pack(side='left',padx=12)
        self.canvas = tk.Canvas(root,bg='#142037',highlightthickness=0)
        self.canvas.pack(fill='both',expand=True,padx=12)
        self.yaw,self.pitch,self.zoom = tk.DoubleVar(value=25),tk.DoubleVar(value=15),tk.DoubleVar(value=1)
        controls = ttk.Frame(root,padding=12)
        controls.pack(fill='x')
        for text,var,start,end in [('Yaw',self.yaw,-180,180),('Pitch',self.pitch,-180,180),('Zoom',self.zoom,.2,2)]:
            ttk.Label(controls,text=text).pack(side='left')
            ttk.Scale(controls,from_=start,to=end,variable=var,command=lambda value:self.draw(),length=180).pack(side='left',padx=8)
        self.status = tk.StringVar(value='Open an OBJ file.')
        ttk.Label(root,textvariable=self.status,padding=12).pack(fill='x')
        self.canvas.bind('<Configure>',lambda event:self.draw())
        self.canvas.bind('<Button-1>',self.start_drag)
        self.canvas.bind('<B1-Motion>',self.drag)
        self.canvas.bind('<MouseWheel>',self.scroll)
        self.canvas.bind('<Button-4>',lambda event:self.scroll_step(1))
        self.canvas.bind('<Button-5>',lambda event:self.scroll_step(-1))
        self.load(Path(__file__).parent/'samples/cube.obj')

    def load(self,path):
        try:
            vertices,edges = load_obj(path)
            self.vertices,self.edges = normalize(vertices),edges
            self.status.set(f'{Path(path).name} · {len(vertices)} vertices · {len(edges)} edges')
            self.draw()
        except (OSError,ValueError) as error:
            messagebox.showerror('Cannot load model',str(error),parent=self.root)

    def open(self):
        path = filedialog.askopenfilename(filetypes=[('OBJ models','*.obj')])
        if path: self.load(path)

    def draw(self):
        self.canvas.delete('all')
        points = project(self.vertices,self.yaw.get(),self.pitch.get(),self.zoom.get(),max(1,self.canvas.winfo_width()),max(1,self.canvas.winfo_height()))
        for a,b in self.edges:
            self.canvas.create_line(*points[a],*points[b],fill='#74cdf1',width=2)

    def reset(self):
        self.yaw.set(25); self.pitch.set(15); self.zoom.set(1)
        self.draw()

    def start_drag(self,event): self.last = (event.x,event.y)

    def drag(self,event):
        x,y = getattr(self,'last',(event.x,event.y))
        self.yaw.set((self.yaw.get()+(event.x-x)*.5+180)%360-180)
        self.pitch.set((self.pitch.get()+(event.y-y)*.5+180)%360-180)
        self.last = event.x,event.y
        self.draw()

    def scroll(self,event): self.scroll_step(1 if event.delta>0 else -1)

    def scroll_step(self,direction):
        self.zoom.set(max(.2,min(2,self.zoom.get()*(1.1 if direction>0 else .9))))
        self.draw()


if __name__ == '__main__':
    root = tk.Tk()
    Viewer(root)
    root.mainloop()
