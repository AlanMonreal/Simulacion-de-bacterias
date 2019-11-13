#! /usr/bin/Rscript

# Correr script de Grind.R
# Cargar deSolve
source("Grind.R")
library(deSolve)

# args = commandArgs(trailingOnly=TRUE)
# if(length(args)==0){
#   stop("No args", call.=FALSE)
# } else if (length(args) >= 1) {
#   print(args[0])
# }

# Declaramos la funcion metiendo nuestro sistema de ecuaciones
ModeloTuberculosis<- function(t, y, parms){  
  MNA_t=y[1];# Macrofago no activado 
  MA_t=y[2];# Macrofago activado
  MNAF_t=y[3];# Macrofago no activado que fagocito
  MAF_t=y[4];# Macrofago activado que fagocito
  TL_t=y[5];# Tuberculosis libre
  TNA_t=y[6];# Tuberculosis en MNAF
  TA_t=y[7]# Tuberculosis en MAF
  
  dMNA<- -MNA_t*(parms[11]+parms[13]*TL_t)# Vida media de macrófago no activado y muerte por M. tuberculosis libre
  -MNA_t*parms[9]# Activación de macrófago no activado
  -MNA_t*TL_t*parms[7]# Fagocitación de M. tuberculosis libre por macrófago no activado
  +MNAF_t*parms[5]+MAF_t*parms[6]# Llegada de macrófago no activado por mecanismos pro-inflamatorios
  +MNA_t*parms[4];# Entrada constante de macrófago no activado
 
  dMA<- -MA_t*(parms[14]+parms[16]*TL_t)# Vida media de macrófago activado y muerte por M. tuberculosis libre 
  -MA_t*TL_t*parms[8]# Fagocitación de M. tuberculosis libre por macrófago activado
  +MNA_t*parms[9];# Activación de macrófago no activado
  
  dMNAF<- -MNAF_t*(parms[17]+parms[20]*TL_t+parms[21]*TNA_t)# Vida media de macrófago no activado que fagocitó y muerte por M. tuberculosis libre y fagocitada 
  -MNAF_t*parms[10]# Activación de macrófago no activado que fagocitó
  +MNA_t*TL_t*parms[7];# Fagocitación de M. tuberculosis libre por macrófago no activado
  
  dMAF<- -MAF_t*(parms[22]+parms[25]*TL_t+parms[26]*TA_t)# Vida media de macrófago activado que fagocitó y muerte por M. tuberculosis libre y fagocitada
  +MNAF_t*parms[10]# Vida media de macrófago activado que fagocitó y muerte por M. tuberculosis libre y fagocitada 
  +MA_t*TL_t*parms[8];# Fagocitación de M. tuberculosis libre por macrófago activado
  
  dTL<- +TL_t*parms[1]# Proliferación de M. Tuberculosis libre
  -TL_t*(parms[27]+parms[12]*MNA_t+parms[15]*MA_t+parms[18]*MNAF_t+parms[23]*MAF_t)# Vida media de M. Tuberculosis libre y muerte por todos los macrófagos que hay en el sistema
  -MA_t*TL_t*parms[8]# Fagocitación de M. Tuberculosis libre por macrófago activo
  -MNA_t*TL_t*parms[7];# Fagocitación de M. Tuberculosis libre por macrófago no activo
  
  dTNA<- +TNA_t*parms[2]# Proliferación de M. Tuberculosis en macrófago no activo
  -TNA_t*(parms[28]+parms[19]*MNAF_t)# Vida media de M. Tuberculosis en M.N.A.F. y muerte por macrófago no activo que fagocitó
  +MNA_t*TL_t*parms[7];# Fagocitación de M. Tuberculosis libre por macrófago no activo
  
  dTA<- +TA_t*parms[3]# Proliferación de M. Tuberculosis en macrófago activo
  -TA_t*(parms[29]+parms[24]*MAF_t)# Vida media de M. Tuberculosis en M.A.F. y muerte por macrófago activo que fagocitó
  +MA_t*TL_t*parms[8]# Fagocitación de M. Tuberculosis libre por macrófago activo
  +MNA_t*parms[10]# Activación de macrófago no activo
  
  list(c(dMNA,dMA,dMNAF,dMAF,dTL,dTNA,dTA))
}

# Declaramos los valores de los parametros

# aTl - Tasa de proliferacion de M. tuberculosis
k1=3;

# aTna - Tasa de proliferacion de M. tuberculosis fagocitada por macrofago no activado
k2=24;

# aTa - Tasa de proliferacion de M. tuberculosis fagocitada por macrofago activado
k3=0.625;

# aM - Entrada constante de macrofago
k4=0.1;

# aMna - Tasa de reclutamiento de monocitos circulantes al lugar de la infección por Macrófago no activado que fagocitó
k5=1;

# aMa - Tasa de reclutamiento de monocitos circulantes al lugar de la infección por Macrófago activado que fagocitó 
k6=3;

# yMna - Capacidad fagocítica de Macrófago no activado
k7=.75;

# yMa - Capacidad fagocítica de Macrófago activado
k8=0.35;

# 0.650 uM - Activación de macrófago que no ha fagocitado
k9=0.650;

# uMf - Activación de macrófago que ha fagocitado
k10=0.90;

# dMna - Vida media de macrofago no activado
k11=17;

# dMnaTl - Tasa de muerte de M. tuberculosis libre causado por Macrófago no activado
k12=48;

# dTlMna - Tasa de muerte de Macrófago no activado causada por M. tuberculosis libre
k13=2;

# dMa - Vida media de macrofago activado
k14=1;

# dMaTl - Tasa de muerte de M. tuberculosis libre causado por Macrófago activado 
k15=1;

# dTlMa - Tasa de muerte de Macrófago activado causada por M. tuberculosis libre
k16=2;

# dMnaf - Vida media de Macrófago no activado que ha fagocitado
k17=1;

# dMnafTl - Tasa de muerte de M. tuberculosis libre causado por Macrófago no activado
k18=12;

# dMnafT - Tasa de muerte de M. tuberculosis fagocitada causado por Macrófago no activado
k19=0.59;

# dTlMnaf - Tasa de muerte de Macrófago no activado que ha fagocitado causada por M. tuberculosis libre
k20=2;

# 0.92 dTMnaf - Tasa de muerte de Macrófago no activado que ha fagocitado causada por M. tuberculosis fagocitada
k21=0.92;

# dMaf - Vida media de Macrófago activado que ha fagocitado
k22=1.3;

# dMafTl - Tasa de muerte de M. tuberculosis libre causado por Macrófago activado que ha fagocitado
k23=5.3;

# MafT - Tasa de muerte de M. tuberculosis fagocitada causado por Macrófago activado que ha fagocitado
k24=0.34;

# TlMaf - Tasa de muerte de Macrófago activado que ha fagocitado causada por M. tuberculosis libre
k25=1.1;

# TMaf - Tasa de muerte de Macrófago activado que ha fagocitado causada por M. tuberculosis fagocitada
k26=19;

# dTl - Vida media de M. tuberculosis libre
k27=2.2;

# dTna - Vida media de M. tuberculosis fagocitada por macrófago no activado
k28=0.33;

# dTa - Vida media de M. tuberculosis fagocitada por macrófago activado
k29=7;


parms=c(k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13, k14, k15,
        k16, k17, k18, k19, k20, k21, k22, k23, k24, k25, k26, k27, k28, k29);

# condiciones iniciales de los nodos de la red
y0=c(5,15,4,2,2,6,3);

# Definimos el intervalo de integracion
tspan =seq(from = 0, to = 12, by = 0.001)

# Integramos con funcion ode
out <- ode(y = y0, times = tspan, func = ModeloTuberculosis, parms = parms)

# Graficamos los resultados
par(pty="s")
plot(out[,1], out[,2], type = "l", col="pink", xlab = "Time", ylab ="[MNA:rosa,MA:rojo, MNAF:azul, MAF:negro, TL:verde, TNA: amarillo, TA:morado]")
lines(out[,1], out[,3],type = "l", col="red")
lines(out[,1], out[,4],type = "l", col="blue")
lines(out[,1], out[,5],type = "l", col="black")
lines(out[,1], out[,6],type = "l", col="green")
lines(out[,1], out[,7],type = "l", col="yellow")
lines(out[,1], out[,8],type = "l", col="purple")


legend=c("X(t)", "Y(t)", "XY(t)")