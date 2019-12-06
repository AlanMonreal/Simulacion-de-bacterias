import tkinter as tk
from tkinter import messagebox
import csv
from r_model import create_r_script
from pdf_maker import make_pdf
import rpy2.robjects as ro
import numpy as np

presetArray = []


class SingleMode(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self)
        self.parent = parent.master
        # self.parent = parent
        # self.pack()
        self.create_widgets()

    def fetch(self, entries):
        values = []
        for entry in entries:
            num = entry.get()
            num = int(num)
            values.append(num)

        fun = create_r_script()
        k = ro.FloatVector(presetArray)
        y0 = ro.IntVector(values)
        output = fun(y0, k)

        result_matrix = np.array(output)  # ARRAY OF ARRAYS
        data_final = [[] for i in range(7)]
        max_data = [[] for i in range(7)]
        tab_data = []
        for data_set in result_matrix:
            temp_arr = []
            for k in range(data_set.size):
                temp_arr.append(data_set[k])
            tab_data.append(temp_arr)
            for i in range(1, data_set.size):
                inserted = data_set[i]  # if data_set[i] < 500 else 500
                data_final[i - 1].append((data_set[0], inserted))
                max_data[i - 1].append(inserted)
        max_val = []
        for j in range(len(data_final)):
            max_val.append(max(max_data[j]))
            data_final[j] = tuple(data_final[j])
        val = max(max_val) / 2
        np.set_printoptions(precision=3)
        np.set_printoptions(suppress=True)
        make_pdf(values, presetArray, data_final, val, tab_data)
        messagebox.showinfo("Exito", "Simulación terminada!")

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
                ent = tk.Label(frame, width=15, text=row[1],
                               background="gray", anchor='w')
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
        buttonGroup = tk.Frame(self)
        btn_preset1 = tk.Radiobutton(buttonGroup, text='Preset 1',
                                     value='presets/preset1.csv', indicator=0,
                                     background="light blue",
                                     command=lambda *args: self.
                                     preset('presets/preset1.csv'))
        btn_preset2 = tk.Radiobutton(buttonGroup, text='Preset 2',
                                     value='preset2.csv', indicator=0,
                                     background="light blue",
                                     command=lambda *args: self.
                                     preset('preset2.csv'))

        buttonGroup.pack(side=tk.RIGHT, fill=tk.X, padx=5, pady=5)
        btn_preset1.pack(side=tk.TOP, fill=tk.X, ipady=5)
        btn_preset2.pack(side=tk.TOP, fill=tk.X, ipady=5)

        # FUNCTION MAKE VAR FORM
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
