from github import Github
import os
from pprint import pprint
from datetime import datetime

token="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" # token de mon compte perso pour accès à distance sans Login/mdp
g = Github(token) # objet sur mon compte TaraLemaire

repoRasp = g.get_repo("TaraLemaire/LogRaspberry") # objet sur le dépôt "LogRaspberry"

file = repoRasp.get_contents("events.log") # objet sur le fichier de logs "events.log"

oldContent = file.decoded_content.decode() # récupérer le contenu du fichier avant modification
print(oldContent) # affichage

date=str(datetime.now())
newContent = oldContent + "\n" + date # Concaténation entre le contenu du fichier et les nouvelles données

repoRasp.update_file("events.log","Commit via Python",newContent,file.sha,branch="main") # push des modifications vers le dépôt
print("Push OK")
print(str(datetime.now())) 
