import sqlite3
import sys
import string
from KAW import KAW
from flask import Flask,request,render_template
#print(sys.version)
import os

#app = Flask(__name__)


#Variables globales
index_Prompts = 0
index_Answers = 0
Number_Of_Players = 3
Players = []

#Variables Felix
judgeid = 1
firstid = 2
secondid = 3
main1 = []
main2 = []
laquestion = ""

#Classe joueur
class Player:
    def __init__(self, Id):
        self.Id = Id
        self.Flag = 0
        self.Cards = []

#Creation des joueurs
def Setup():
	global Number_Of_Players
	global Players
	global index_Answers
	    
	#Pour le nombre de joueurs entre
	    #Les cartes de depart lui sont attribuees
	    #for num in range(0,Number_Of_Players):
	for num in range(1,4):
		x = Player(num)                                       #Un objet Player est cree avec l'index actuel
		x.Cards.append(Answers[index_Answers:index_Answers+9])#Attribtion des cartes de depart
		Players.append(x)                                     #Ajout de l'objet Player a la liste Players
		index_Answers = index_Answers +9                     #Incrementation de l'indice pour le tableau de cartes de reponse
	return

#Connexion a la basse de donnee
connection = sqlite3.connect("/home/trygle/python/KAW/CAH_db")

#Creation d'un curseur pour interactions
cursor = connection.cursor()


#Execution d'un commande. P correspondra a une quatite fixe de donnees aleatoires contenus dans la table prompts_example
P = cursor.execute ("""
SELECT Prompt
FROM prompts_example
ORDER BY RANDOM() LIMIT 25""")

#Ajout des donnees obtenues dans la liste Prompts
Prompts = P.fetchall()


#Execution d'un commande. A correspondra a une quatite fixe de donnees aleatoires contenus dans la table answers_example
A = cursor.execute ("""
SELECT Answer
FROM answers_example
ORDER BY RANDOM() LIMIT 250""")

#Ajout des donnees obtenues dans la liste Prompts
Answers = A.fetchall()

#Fermeture de la connexion avec la base de donnee
connection.close()

#Population de la liste Players avec un nombre d'objet Player obtenu en parametre
#Players = [[Player]*Number_Of_Players]

Setup()

@KAW.route('/')
@KAW.route('/kaw_tour', methods=['POST'])
def kawturn():
	global judgeid
	global firstid
	global secondid
	global main1
	global main2
	global laquestion
	global Players
	global index_Prompts
	
	laquestion = Prompts[0][0]
	
	main1 = [x[0] for x in Players[1].Cards[0]]
	main2 = [x[0] for x in Players[2].Cards[0]]
	judgeid = Players[0].Id
	firstid = Players[1].Id
	secondid = Players[2].Id
	index_Prompts = index_Prompts + 1
	'''
	judgeid = Players[0].Id[0]
	firstid = Players[1].Id[0]
	secondid = Players[2].Id[0]
	'''

	return render_template("formulairetour.html", judge = judgeid, question = laquestion, firstplayer = firstid, firsthand = main1, secondplayer = secondid, secondhand = main2)

@KAW.route("/kaw_verdict", methods=['POST'])
def kawjudge():
	global judgeid
	global firstid
	global secondid
	global main1
	global main2
	global laquestion
	choix1 = int(request.form['choix1'])
	choix2 = int(request.form['choix2'])
	laselection = []
	laselection.append(main1[choix1-1])
	laselection.append(main2[choix2-1])
	return render_template("formulaireverdict.html",judge = judgeid, question = laquestion, selection = laselection)


@KAW.route('/kaw_winner', methods=['POST'])
def kawvictor():
	joueurgagnant = request.form['choix']
	return render_template("formulairegagnant.html", winner = joueurgagnant)

