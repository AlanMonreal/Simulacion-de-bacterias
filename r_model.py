import rpy2.robjects as ro


def create_r_script():
    print(' ------------------------------ creating R script ----------------')
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
                tspan = seq(from = 0, to = 12, by = 1)
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

                #par(pty = "s")
                #plot(out[,1], out[,2], type = "l", col="pink", xlab = "Time",
                #     ylab ="[MNA:rosa,MA:rojo, MNAF:azul, MAF:negro, TL:verde,
                #     TNA: amarillo, TA:morado]")
                #lines(out[,1], out[,3], type = "l", col = "red")
                #lines(out[,1], out[,4], type = "l", col = "blue")
                #lines(out[,1], out[,5], type = "l", col = "black")
                #lines(out[,1], out[,6], type = "l", col = "green")
                #lines(out[,1], out[,7], type = "l", col = "yellow")
                #lines(out[,1], out[,8], type = "l", col = "purple")
                #legend = c("X(t)", "Y(t)", "XY(t)")
                return(resp)
            }
        ''')

    run_f = ro.globalenv['run']
    return run_f
