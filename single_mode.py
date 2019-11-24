import tkinter as tk


class SingleMode(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self)
        self.parent = parent.master
        # self.parent = parent
        # self.pack()
        self.create_widgets()

    def fetch(self, entries):
        results = []
        for entry in entries:
            num  = entry.get()
            num = int(num)
            results.append(num)
        print(results)
        return results

    def makeform(self, fields):
        entries = []
        for field in fields:
            row = tk.Frame(self)
            lab = tk.Label(row, width=15, text=field, anchor='w')
            ent = tk.Entry(row)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries.append(ent)
        return entries

    def create_widgets(self):
        fields = ['var1','var2','var3']
        entries = self.makeform(fields)
        b1 = tk.Button(self, text='Show',
                      command=lambda:self.fetch(entries))
        self.quit = tk.Button(self, text="SALIR", fg="red",
                              command=self.destroy)
        b1.pack(side="left", padx=30, pady=10)
        self.quit.pack(side="right", padx=30, pady=10)
