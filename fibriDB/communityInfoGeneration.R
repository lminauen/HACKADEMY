library(readr)
library(stringr)
library(dplyr)

rm(list=ls())

community_id <- read_csv("data/community_ids.csv")
colnames(community_id) <- c("ID", "Ort", "Kanton")
community <- read_csv("data/municipalities.csv")

D <- merge(community_id, community, by=c("Ort", "Kanton"))
D <- select(D, c("ID", "PLZ"))
id <- 1:nrow(D)
D$id <- id

D <- D[,c(3,2,1)]
colnames(D) <- c("id", "postalCode", "commune_id")

write_csv(D, "data/communityinfo.csv")
