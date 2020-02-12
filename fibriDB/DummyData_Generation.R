library(readr)
library(stringr)
library(dplyr)

rm(list=ls())

community_list <- read_csv("municipalities.csv")
id_list <- unique(community_list[,c(2,3)])
id_list <- mutate(id_list, id = 1:nrow(id_list))

colnames(id_list) <- c("Ort", "Kanton", "ID")
colnames(community_list) <- c("PLZ", "Ort", "Kanton")
community_list <- community_list[, c(2,1,3)]

D <- left_join(community_list, id_list, by = c("Ort", "Kanton"))

write_csv(D, "communities.csv")
write_csv(id_list, "community_ids.csv")

#check if correct
# test <- unique(D[,c(1,4)])
# for(i in unique(test$Ort)){
#   if(length(which(test$Ort == i))>1){
#     print("Error!")
#   }
#}



#generate user data
users <- data.frame(c(1:nrow(id_list)))
colnames(users) <- "ID"

streetnames <- c("Poststrasse", "Bahnhofstrasse", "Marktgasse", "Zürcherstrasse", "Marktplatz", "Usterstrasse", "Werdstrasse",
                "Morgartenstrasse", "Rue de la Croix-Rouge", "Rue du Château", "Place de l'hôtel", "Rue de l'hôpital", "Piazza Riforma",
                "Via Trevano", "Hirschengraben", "Bärenplatz", "Industriestrasse", "Winkelriedstrasse", "Tellstrasse", "Dufourstrasse")
streetlist <- paste(sample(streetnames, nrow(users), replace = T), sample(c(1:100), nrow(users), replace = T))
language <- sample(c("DE", "FR", "IT"), nrow(users), replace = T)
pc <- data.frame(id_list$Ort)
pc <- mutate(pc, PLZ = "")
for(i in 1:nrow(pc)){
  pc[i,2] = D[[min(which(D$Ort == pc[i,1])),2]]
}

pc <- pc[,2]
users <- users %>% mutate(username = paste(str_replace(id_list$Ort, " ", "_"), str_replace(id_list$Kanton, " ", "_"), "admin", sep = "_")) %>%
  mutate(mail = tolower(paste("mail_", str_replace(id_list$Ort, " ","_" ), "@", id_list$Kanton, ".ch", sep =""))) %>%
  mutate(language = language, street = streetlist, PLZ = pc)
rm(pc, language, streetlist, streetnames, i)

write_csv(users, "userData.csv")


#Defibrillator Data


defib <- read_csv("../completeDummy.csv")
defib <- defib[,c(4:7, 10:14)]
defib <- na.omit(defib)

ind <- apply(defib, 1, function(x) all(is.na(x)))
defib <- defib[ !ind, ]
rm(ind)
defib <- defib[-98,] #only column with a special case

defib <- defib %>% mutate(ID = c(1:nrow(defib)))
colnames(defib) <- c("PLZ", 2:9, "ID")
defib <- defib[,c(10, 1:9)]

defib[,2] <- sapply(defib[,2], as.numeric)

dummyDefib <- merge(defib, D[,c(2:4)], by = "PLZ", all.x = T)
dummyDefib <- dummyDefib[with(dummyDefib, order(ID.x)),]
row.names(dummyDefib) <- NULL

rm(defib)

dummyDefib <- mutate(dummyDefib, type = 1)
dummyDefib <- dummyDefib[, c(2, 13, 12, 9, 10, 1, 3:5, 11, 6:8)]

colnames(dummyDefib) <- c("ID", "type", "community_ID", "latitude", "longitude", "PLZ", "Ort", "Adresse", "Nr", "Kanton",
                         "Ort_Beschreibung", "Bemerkung", "Zuständigkeit")
write_csv(dummyDefib, "dummyDefib.csv")

