import tkinter as tk
from tkinter import messagebox
import csv
from r_model import create_r_script
import rpy2.robjects as ro
import numpy as np
from csv_maker import create_csv


class BatchMode(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self)
        self.parent = parent.master
        self.create_widgets()

    def fetch(self, entries):
        ini_var = []
        for entry in entries:
            num1 = entry[0].get()
            num1 = int(num1)
            num2 = entry[1].get()
            num2 = int(num2)
            values = num1, num2
            ini_var.append(values)
        print(ini_var)
        print(presetArray)
        a1 = self.make_arr(0, ini_var)
        a2 = self.make_arr(1, ini_var)
        a3 = self.make_arr(2, ini_var)
        a4 = self.make_arr(3, ini_var)
        a5 = self.make_arr(4, ini_var)
        a6 = self.make_arr(5, ini_var)
        a7 = self.make_arr(6, ini_var)
        meshgrid = np.meshgrid(a1, a2, a3, a4, a5, a6, a7)
        data = np.array(meshgrid).T.reshape(-1, 7)
        print(data)
        fun = create_r_script()
        k = ro.FloatVector(presetArray)
        final = []
        for it in data:
            y0 = ro.IntVector(it)
            output = fun(y0, k)
            result_matrix = np.array(output)
            final.append(result_matrix)
        create_csv(final)
        messagebox.showinfo("Exito", "Simulación terminada!")

    def makeform(self, fields):
        entries = []
        for field in fields:
            row = tk.Frame(self)
            spin = tk.Frame(self)
            lab = tk.Label(row, width=15, text=field, anchor='w')
            _from = tk.Spinbox(row, width=15, from_=0, to=100)
            _to = tk.Spinbox(row, width=15, from_=0, to=100)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            spin.pack(side=tk.RIGHT, fill=tk.X, padx=5, pady=5)
            _from.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
            _to.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            value = [_from, _to]
            entries.append(value)
        return entries

    def preset(self, file):
        global presetArray
        array = []
        i = 2
        j = 1
        loop = 0
        frame = tk.Frame(self)
        title = tk.Label(frame, width=15, text="PRESET VALUES:", anchor='w')
        title.grid(row=1)
        with open(file, 'r') as f:
            reader = csv.reader(f)  # change contents to floats
            for row in reader:  # each row is a list
                if (j == 7):
                    j = 1
                lab = tk.Label(frame, width=15, text=row[0], anchor='w')
                ent = tk.Label(frame, width=15, text=row[1], background="gray",
                               anchor='w')
                lab.grid(row=i, column=j, padx=5, pady=5)
                j += 1
                ent.grid(row=i, column=j, padx=5, pady=5)
                j += 1
                loop += 1
                if (loop % 3 < 1):
                    i += 1
                array.append(float(row[1]))
        frame.pack(side=tk.LEFT, padx=15, pady=5)
        presetArray = array

    def create_widgets(self):
        fields = ['MNA', 'MA', 'MNAF', 'MAF', 'TL', 'TNA', 'TA']
        # FRAME PRESET BUTTONS
        btn_G = tk.Frame(self)
        btn_p1 = tk.Radiobutton(btn_G, text='Preset 1', value='preset1.csv',
                                indicator=0, background="light blue",
                                command=lambda *args: self.
                                preset('presets/preset1.csv'))
        btn_p2 = tk.Radiobutton(btn_G, text='Preset 2', value='preset2.csv',
                                indicator=0, background="light blue",
                                command=lambda *args: self.
                                preset('presets/preset2.csv'))
        btn_G.pack(side=tk.RIGHT, fill=tk.X, padx=5, pady=5)
        btn_p1.pack(side=tk.TOP, fill=tk.X, ipady=5)
        btn_p2.pack(side=tk.TOP, fill=tk.X, ipady=5)
        # VARIABLE ENTRIES
        entries = self.makeform(fields)
        # BUTTONS FRAME
        bottom = tk.Frame(self)
        btn_show = tk.Button(bottom, text='Show',
                             command=lambda: self.fetch(entries))

        self.quit = tk.Button(bottom, text="SALIR", fg="red",
                              command=self.destroy)
        bottom.pack(side="bottom")
        btn_show.pack(side="left", padx=30, pady=10)
        self.quit.pack(side="right", padx=30, pady=10)

    def make_arr(self, n, data):
        rang = range(data[n][0], data[n][1] + 1)
        result = []
        for i in rang:
            result.append(i)
        return np.array(result).flatten()
