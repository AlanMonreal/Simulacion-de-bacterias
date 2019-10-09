import tkinter as tk


class SingleMode(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self)
        self.parent = parent.master
        # self.parent = parent
        # self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.single_mode = tk.Button(self)
        self.single_mode["text"] = "MODO SIMPLE"
        # self.single_mode["command"] = self.launch_single_mode
        self.single_mode.pack(side="top")

        self.batch_mode = tk.Button(self)
        self.batch_mode["text"] = "MODO INVESTIGACIÓN"
        # self.batch_mode["command"] = self.launch_batch_mode
        self.batch_mode.pack(side="top")

        self.quit = tk.Button(self, text="SALIR", fg="red",
                              command=self.parent.destroy)
        self.quit.pack(side="bottom")
