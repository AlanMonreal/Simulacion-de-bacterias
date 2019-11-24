import tkinter as tk
from single_mode import SingleMode
from batch_mode import BatchMode
# from rpy2.robjects.packages import STAP
import rpy2.robjects as ro
import numpy as np
import csv


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
        create_r_script()

    def launch_batch_mode(self):
        self.batch = BatchMode(self)
        self.batch.wm_title("MODO INVESTIGACIÓN")


def create_r_script():
    # ModeloTuberculosis<- function(t, y, parms){
    # y0 = c(5, 15, 4, 2, 2, 6, 3)
    # parms = c(k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13,
    #           k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, k24, k25,
    #           k26, k27, k28, k29)
    # k1 <- 3
    # k2 <- 24
    # k3 <- 0.625
    # k4 <- 0.1
    # k5 <- 1
    # k6 <- 3
    # k7 <- 0.75
    # k8 <- 0.35
    # k9 <- 0.650
    # k10 <- 0.90
    # k11 <- 17
    # k12 <- 48
    # k13 <- 2
    # k14 <- 1
    # k15 <- 1
    # k16 <- 2
    # k17 <- 1
    # k18 <- 12
    # k19 <- 0.59
    # k20 <- 2
    # k21 <- 0.92
    # k22 <- 1.3
    # k23 <- 5.3
    # k24 <- 0.34
    # k25 <- 1.1
    # k26 <- 19
    # k27 <- 2.2
    # k28 <- 0.33
    # k29 <- 7
    # tspan = seq(from = 0, to = 12, by = 0.01)
    print('creating R script')
    ro.r('''
            source("Grind.R")
            library(deSolve)

            model <- function(t, y, parms){
                MNA_t  <- y[1]
                MA_t   <- y[2]
                MNAF_t <- y[3]
                MAF_t  <- y[4]
                TL_t   <- y[5]
                TNA_t  <- y[6]
                TA_t   <- y[7]

                dMNA <- -MNA_t*(parms[11]+parms[13]*TL_t)
                    -MNA_t*parms[9]
                    -MNA_t*TL_t*parms[7]
                    +MNAF_t*parms[5]+MAF_t*parms[6]
                    +MNA_t*parms[4]

                dMA <- -MA_t*(parms[14]+parms[16]*TL_t)
                    -MA_t*TL_t*parms[8]
                    +MNA_t*parms[9];

                dMNAF <- -MNAF_t*(parms[17]+parms[20]*TL_t+parms[21]*TNA_t)
                    -MNAF_t*parms[10]
                    +MNA_t*TL_t*parms[7];

                dMAF <- -MAF_t*(parms[22]+parms[25]*TL_t+parms[26]*TA_t)
                    +MNAF_t*parms[10]
                    +MA_t*TL_t*parms[8];

                dTL <- +TL_t*parms[1]
                    -TL_t*(parms[27]+parms[12]*MNA_t+parms[15]*MA_t+parms[18]*MNAF_t+parms[23]*MAF_t)
                    -MA_t*TL_t*parms[8]
                    -MNA_t*TL_t*parms[7];

                dTNA <- +TNA_t*parms[2]
                    -TNA_t*(parms[28]+parms[19]*MNAF_t)
                    +MNA_t*TL_t*parms[7];

                dTA <- +TA_t*parms[3]
                    -TA_t*(parms[29]+parms[24]*MAF_t)
                    +MA_t*TL_t*parms[8]
                    +MNA_t*parms[10]

                list(c(dMNA,dMA,dMNAF,dMAF,dTL,dTNA,dTA))
            }

            run <- function(y, k){
                parms = k
                y0 = y
                tspan = seq(from = 0, to = 5, by = 0.5)
                out <- ode(y = y0, times = tspan, func = model,
                       parms = parms)

                time <- c(out[,1])
                MNA  <- c(out[,2])
                MA   <- c(out[,3])
                MNAF <- c(out[,4])
                MAF  <- c(out[,5])
                TL   <- c(out[,6])
                TNA  <- c(out[,7])
                TA   <- c(out[,8])
                resp <- cbind(c(out[,1]), c(out[,2]), c(out[,3]), c(out[,4]),
                              c(out[,5]), c(out[,6]), c(out[,7]), c(out[,8]))

                # print(resp)

                par(pty = "s")
                plot(out[,1], out[,2], type = "l", col="pink", xlab = "Time",
                     ylab ="[MNA:rosa,MA:rojo, MNAF:azul, MAF:negro, TL:verde,
                     TNA: amarillo, TA:morado]")
                lines(out[,1], out[,3], type = "l", col = "red")
                lines(out[,1], out[,4], type = "l", col = "blue")
                lines(out[,1], out[,5], type = "l", col = "black")
                lines(out[,1], out[,6], type = "l", col = "green")
                lines(out[,1], out[,7], type = "l", col = "yellow")
                lines(out[,1], out[,8], type = "l", col = "purple")
                legend = c("X(t)", "Y(t)", "XY(t)")
                return(resp)
            }
        ''')

    run_f = ro.globalenv['run']
    y0 = ro.IntVector([479, 380, 6, 3, 900, 8, 9])
    k = ro.FloatVector([3, 24, 0.625, 0.1, 1, 3, 0.75, 0.35, 0.650, 0.90, 17,
                        48, 2, 1, 1, 2, 1, 12, 0.59, 2, 0.92, 1.3, 5.3, 0.34,
                        1.1, 19, 2.2, 0.33, 7])
    output = run_f(y0, k)
    matrix = np.array(output)  # ARRAY OF ARRAYS

    for data_set in matrix:
        print(data_set)


results = []
# TODO: CHANGE FILE NAME DYNAMICALLY - ADD TO FUNCTION
with open("input.csv") as csvfile:
    # change contents to floats
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:  # each row is a list
        for item in row:
            results.append(item)
# root = tk.Tk()
# root.title("Simulador de bacterias")
# root.geometry("300x150+500+300")
# app = Welcome(root)
# app.mainloop()
create_r_script()
