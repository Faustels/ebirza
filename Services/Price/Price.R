#Pirmas bandymas Rshiny dashboard
library(readxl)
unlink("Data", recursive = TRUE)
dir.create("Data")
duom=read_excel("duom.xlsx")
for (tempI in 0:23) {
  i = tempI * 2 + 1
  duom1=duom[,c(i,i+1)]
  Buy=duom1[seq(which(duom1[,1]=="Buy curve")+1,which(duom1[,1]=="Sell curve")-1, by=1),]
  if(is.na(which(is.na(duom1[,1]))[1])){
    galas=nrow(duom1)
  } else{
    galas=which(is.na(duom1[,1]))[1]-1
  }
  Sell=duom1[seq(which(duom1[,1]=="Sell curve")+1,galas,by=1),]
  BuyX=as.vector(apply(Buy[which(Buy[,1]=="Volume value"),2], 2, as.numeric))
  BuyY=as.vector(apply(Buy[which(Buy[,1]=="Price value"),2], 2, as.numeric))
  SellX=as.vector(apply(Sell[which(Sell[,1]=="Volume value"),2], 2, as.numeric))
  SellY=as.vector(apply(Sell[which(Sell[,1]=="Price value"),2], 2, as.numeric))
  dir.create(paste("Data/",tempI, sep=""))
  
  fileName = paste("Data/",tempI, "/BuyX.txt", sep="")
  file.create(fileName, showWarnings = TRUE)
  write(BuyX, file = fileName, ncolumns=length(BuyX))
  
  fileName = paste("Data/",tempI, "/BuyY.txt", sep="")
  file.create(fileName, showWarnings = TRUE)
  write(BuyY, file = fileName, ncolumns=length(BuyY))
  
  
  fileName = paste("Data/",tempI, "/SellX.txt", sep="")
  file.create(fileName, showWarnings = TRUE)
  write(SellX, file = fileName, ncolumns=length(SellX))
  fileName = paste("Data/",tempI, "/SellY.txt", sep="")
  file.create(fileName, showWarnings = TRUE)
  write(SellY, file = fileName, ncolumns=length(SellY))
}