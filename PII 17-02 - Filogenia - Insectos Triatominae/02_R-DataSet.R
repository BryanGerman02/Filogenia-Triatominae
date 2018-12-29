#Este script se utiliza para la creación de un vector de n-gramas que servirán para la selección de características
#morfológicas de los insectos vectores de la enfermedad del Chagas


#Librerías utilizadas para:
#1. Text mining
library(tm)
#2. Creación de N-gramas
library(RWeka)

#Lectura de los archivos necesarios para crear los n-gramas
path = "C:/Users/bryan/Documents/GitHub/Filogenia-Triatominae/descriptions_separated_files/"
dir = DirSource(paste(path,"/",sep=""), encoding = "UTF-8")
corpus = VCorpus(dir)

#Creación de los n-gramas con sus parámetros necesarios
BigramTokenizer <- function(x) NGramTokenizer(x, Weka_control(min = 1, max = 5))
tdm.bigram = TermDocumentMatrix(corpus,control = list(tolower = FALSE,removeNumbers= T, removePunctuation = T ,stripWhitespace = T, tokenize = BigramTokenizer))

#Exportar los n-gramas con su frecuencia en cada documento
write.table(as.matrix(tdm.bigram), file = "C:/Users/bryan/Documents/GitHub/Filogenia-Triatominae/filesData.csv",sep = ",")