#Marc-Andre Labrosse
#Felix St-Amour


import sqlite3
import sys
import string
#print(sys.version)

#Variables globales
index_Prompts = 0
index_Answers = 0
Number_Of_Players = 0
Players = []

#Classe joueur
class Player:
    def __init__(self, Id):
        self.Id = Id
        self.Cards = []

#Creation des joueurs
def Setup():
    global Number_Of_Players
    global Players
    global index_Answers

    #Requete pour obtenir le nombre de joueur
    Number_Of_Players = (int)(input("Enter number of players (3-4)"))

    #Pour le nombre de joueurs entre
    #Les cartes de depart lui sont attribuees
    for num in range(0,Number_Of_Players):
        x = Player(num)                                       #Un objet Player est cree avec l'index actuel
        x.Cards.append(Answers[index_Answers:index_Answers+9])#Attribtion des cartes de depart
        Players.append(x)                                     #Ajout de l'objet Player a la liste Players
        index_Answers = index_Answers +9                      #Incrementation de l'indice pour le tableau de cartes de reponse
    return

#creation d'un joueur
def MakePlayer(username):
    global Number_Of_Players
    global Players
    global index_Answers
    x = Player(username)                                   #Un objet Player est cree avec l'index actuel
    x.Cards.append(Answers[index_Answers:index_Answers+9]) #Attribtion des cartes de depart
    Players.append(x)                                     #Ajout de l'objet Player a la liste Players
    index_Answers = index_Answers +9                     #Incrementation de l'indice pour le tableau de cartes de reponse
    Number_Of_Players += 1
    return None

#Connexion a la basse de donnee
connection = sqlite3.connect("CAH_db")

#Creation d'un curseur pour interactions
cursor = connection.cursor()


#Execution d'un commande. P correspondra a une quatite fixe de donnees aleatoires contenus dans la table prompts_example
P = cursor.execute ("""
SELECT Prompt
FROM prompts_example
ORDER BY RANDOM() LIMIT 5""")

#Ajout des donnees obtenues dans la liste Prompts
Prompts = P.fetchall()


#Execution d'un commande. A correspondra a une quatite fixe de donnees aleatoires contenus dans la table answers_example
A = cursor.execute ("""
SELECT Answer
FROM answers_example
ORDER BY RANDOM() LIMIT 50""")

#Ajout des donnees obtenues dans la liste Prompts
Answers = A.fetchall()

#Fermeture de la connexion avec la base de donnee
connection.close()

#Population de la liste Players avec un nombre d'objet Player obtenu en parametre
Players = [[Player]*Number_Of_Players]

if __name__ == '__main__':
    name = ""
    while( name != "GO"):
        name =  input("entre un nom de joueur: ")
        if ( name != "GO"):
            MakePlayer(name)

    #Setup()
    print(Number_Of_Players)
    print("Question")
    print(Prompts[0])
    index_Prompts = index_Prompts + 1
    print("\n\r\n\r") 
    
    print(Players)
    # line_iter = iter(Players[:-1])                        #Creation d'un iterateur
    # for index, Player in enumerate(line_iter, start=1):   #Pour chaque joueur dans la liste Players (on obtient aussi l'index du Player dans la liste)
    #     print("Player ",index)                            #Impression de l'index du joueur
    #     for num, Card in enumerate(Players[index].Cards): #Impression de chaque carte possedee par les Joueurs
    #         print(Card)
    #     print("\n\r\n\r")