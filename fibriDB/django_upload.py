import os
import django
import pandas as pd
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibriDB.settings')
django.setup()

from mainApp.models import User, UserProfileInfo, items, community_id, community, type

def populate():
    itemsData = pd.read_csv("dummyDefib.csv")
    userData = pd.read_csv("userData.csv")
    communityIDData = pd.read_csv("community_ids.csv")
    communityData = pd.read_csv("municipalities.csv")

    #for i in range(len(communityIDData)):
        #print("Added category "+str(i)+"/"+str(len(communityIDData)))
        #name = communityIDData.Ort[i]
        #canton = communityIDData.Kanton[i]
        #community_id.objects.get_or_create(name=name, canton=canton)

    #name = "default"
    #type.objects.get_or_create(name=name)
    #print("Added type")

    #for i in range(len(userData)):
        #print("Added category "+str(i)+"/"+str(len(userData)))
        #id = userData.ID[i]
        #username = userData.username[i]
        #print(username)
        #print(id)
        #mail = userData.mail[i]
        #language = userData.language[i]
        #if not str(userData.street[i]):
            #address = None
        #else:
            #address = userData.street[i]
        #if not str(userData.PLZ[i]):
            #pc = None
        #else:
            #pc = userData.PLZ[i]
        #User.objects.get_or_create(username=username, password="1234", email = mail)
        #UserProfileInfo.objects.get_or_create(user=User.objects.get(username=username), postalCode=pc, street=address, language=language)


    for i in range(len(communityData)):
        print("Added category"+str(i)+"/"+str(len(communityData)))
        name = communityData.Ort[i]
        pc = communityData.PLZ[i]
        community.objects.get_or_create(postalCode=pc, commune_id=community_id.objects.get(name=name).id)


    #for i in range(len(itemsData)):
        #print("Added category "+str(i)+"/"+str(len(itemsData)))
        #id = itemsData.ID[i]
        #type_name = itemsData.type[i]
        #community = itemsData.community_ID[i]
        #latitude = itemsData.latitude[i]
        #longitude = itemsData.longitude[i]
        #pc = itemsData.PLZ[i]
        #location = itemsData.Ort[i]
        #if not str(itemsData.Nr[i]):
            #address = itemsData.Adresse[i]
        #else:
            #address = itemsData.Adresse[i] + " " + itemsData.Nr[i]
        #canton = itemsData.Kanton[i]
        #if not str(itemsData.Ort_Beschreibung[i]):
            #location_descr = None
        #else:
            #location_descr = itemsData.Ort_Beschreibung[i]
        #if not str(itemsData.Bemerkung[i]):
            #notes = None
        #else:
            #notes = itemsData.Bemerkung[i]
        #if not str(itemsData.Zuständigkeit[i]):
            #responsible = None
        #else:
            #responsible = itemsData.Zuständigkeit[i]
        #items.objects.get_or_create(type=type.objects.get(id=1), user_id=2470, community_id=1794, latitude=latitude, longitude=longitude, pc=pc, location=location, address=address, canton=canton,
        #location_descr=location_descr, notes=notes, responsible=responsible)


print("Populating")
populate()
print('Finished Populating')
