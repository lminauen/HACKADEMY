library(readr)
library(stringr)
library(dplyr)

rm(list = ls())
dummy <- read_csv("data/dummyDefib.csv")
id <- c(1:nrow(dummy))
dummy$newID <- id
dummy <- select(dummy, -c("ID"))
dummy <- dummy[,c(13,1:12)]
colnames(dummy)[1] <- c("ID")


model <- sample(1:4, nrow(dummy), replace =T)
attributesdefib <- data.frame(c(1:nrow(dummy)), c(1:nrow(dummy)), model)
colnames(attributesdefib) <- c("id", "item_id", "model_id")


write_csv(attributesdefib, "data/attributesdefib.csv")
