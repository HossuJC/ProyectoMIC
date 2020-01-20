
library('Hmisc')
library(dplyr)
library(readr)
#datos <- read_csv(file="AreasNaturalezayVidaSilvestre.csv")
#datos<- read.table(file = "AreasNaturalezayVidaSilvestre.csv", header = TRUE, sep = "|", dec = ".")

datos <- read_delim(file="Nombre.csv",delim  =  "|",col_names = TRUE )
#View(datos)
datos<-datos[complete.cases(datos),]

#num<- c(FALSE,FALSE,FALSE,FALSE,TRUE,FALSE)
#datos[,num]= as.double(datos$Calificacion) # lo conviertes a numérico

View(datos)

datos <- datos[with(datos, order(-datos$Calificacion)), ] #Ordena los datos de mayor a menor


datosSinRep <- datos[!duplicated(datos), ] #Elimina los comentarios repetidos

mediaCal <-mean(datosSinRep$Calificacion) #Media de las calificaciones
View(mediaCal)
#View(datosSinRep)

#Codificación para el texto de los comentarios y categorías
enc2utf8(datosSinRep$Categoria)
enc2utf8(datosSinRep$Comentario)


write_delim(datosSinRep,"Otros Ordenado.csv", delim = "|", append = FALSE) #Guardar los datos

