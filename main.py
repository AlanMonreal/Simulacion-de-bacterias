import tkinter as tk
from single_mode import SingleMode
from batch_mode import BatchMode


class Welcome(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.single_mode = tk.Button(self)
        self.single_mode["text"] = "MODO SIMPLE"
        self.single_mode["command"] = self.launch_single_mode
        self.single_mode.pack(side="top")

        self.batch_mode = tk.Button(self)
        self.batch_mode["text"] = "MODO INVESTIGACIÓN"
        self.batch_mode["command"] = self.launch_batch_mode
        self.batch_mode.pack(side="top")

        self.quit = tk.Button(self, text="SALIR", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def launch_single_mode(self):
        self.single = SingleMode(self)
        self.single.wm_title("MODO SIMPLE")
        # root.withdraw()

    def launch_batch_mode(self):
        self.batch = BatchMode(self)
        self.batch.wm_title("MODO INVESTIGACIÓN")


root = tk.Tk()
root.title("Simulador de bacterias")
root.geometry("200x150+500+300")
app = Welcome(root)
app.mainloop()
