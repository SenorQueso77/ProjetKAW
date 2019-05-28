#
#						    Projet KAW
#							   par
#						  Félix St-Amour
#							   et
#						Marc-André Labrosse
#

import sqlite3
import sys
import string
import os
import random
import time
import datetime
import netifaces as ni
import lxml.html
from flask import Flask,request,render_template
from flask_socketio import SocketIO

app = Flask(__name__)										#initialisation de flask

#Variables globales
index_Prompts = 0
index_Answers = 0
Number_Of_Players = 0
Players = []												#tableau contenant les mains et les Id des joueurs
judgeid = ""												#variable pour l'identité du juge
laquestion = ""												#variable pour la question
joueurgagnant = ""											#variable pour l'identité du joueur gagnant
selection = []												#liste des réponses pour le juge
selectId = []												#liste des Id qui ont soumis les réponse

#Classe joueur
class Player:
    def __init__(self, Id):
        self.Id = Id
        self.Flag = 0
        self.Cards = []

#creation d'un joueur
def AddPlayer(username):
	global Number_Of_Players
	global Players
	global index_Answers
	Number_Of_Players = Number_Of_Players +1
	x = Player(username)                                   #Un objet Player est cree avec l'index actuel
	x.Cards.append(Answers[index_Answers:index_Answers+9]) #Attribtion des cartes de depart
	Players.append(x)                                     #Ajout de l'objet Player a la liste Players
	index_Answers = index_Answers +9                     #Incrementation de l'indice pour le tableau de cartes de reponse
	return None

#Connexion a la basse de donnee
connection = sqlite3.connect("/home/debian/ProjetKAW/CAH_db")

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

@app.route('/')
@app.route('/kaw_log', methods=['POST'])
def kawlogin():
	return render_template("formulaireinit.html")

@app.route('/kaw_lobby', methods=['POST'])
def kawlobby():
	global judgeid
	global Players
	global laquestion

	laquestion = Prompts[0][0]									#initialise la question
	user = request.form['username']								#va chercher le username de l'utilisateur
	AddPlayer(user)												#création du joueur
	Plist = []													

	for a in range(0, int(len(Players))):
		Plist.append(Players[a].Id)								#ajoute le Id du Joueur à la liste des joueurs pour le lobby
	judgeid = Players[0].Id 									#identifie le premier joueur comme le juge

	return render_template("formulairelobby.html", user = user, Plist = Plist)

@app.route('/kaw_tour', methods=['POST'])
def kawturn():
	global judgeid
	global laquestion
	global Players
	global selectId
	global index_Prompts
	
	P_hand = []
	selectId = []
	
	
	user = request.form['username']								#va chercher le username de l'utilisateur
	
	for a in range(0, int(len(Players))):
		if(Players[a].Id == user):								#cherche le tableau pour le joueur
			P_hand = [x[0] for x in Players[a].Cards[0]]		#met la main du joueur dans le tableau pour la page html
			break

	if(user == judgeid):										#si le joueur est le juge
		PAGE = "formulairejudge.html"							#load la page d'attente du juge
	else:
		PAGE = "formulairetour.html"							#load la page de selection des cartes

	return render_template(PAGE, judge = judgeid, question = laquestion, user = user, hand = P_hand)

@app.route("/kaw_verdict", methods=['POST'])
def kawjudge():
	global judgeid
	global laquestion
	global selection
	global selectId
	global Players
	global joueurgagnant
	global index_Answers
	global index_Prompts

	joueurgagnant = ""
	user = request.form['username']								#va chercher le username de l'utilisateur
	choix = int(request.form['choix'])							#va chercher le choix de l'utilisateur

	if(user == judgeid):										#si le joueur est le juge
		PAGE = "formulaireverdict.html"
	else:
		PAGE = "formulairewait.html"
		for a in range(0, int(len(Players))):				
			if(Players[a].Id == user):
				P_hand = [x[0] for x in Players[a].Cards[0]]	
				del Players[a].Cards[0][choix-1]				#enleve la carte jouer
				Players[a].Cards[0].append(Answers[index_Answers])#ajoute une nouvelle carte
				index_Answers = index_Answers +1
				selection.append(P_hand[choix-1])				#met dans une liste la carte selectionnée
				selectId.append(Players[a].Id) 					#met dans une liste le username pour identifié qui a jouer la carte
				break

	return render_template(PAGE,judge = judgeid, question = laquestion, selection = selection)


@app.route('/kaw_winner', methods=['POST'])
def kawvictor():
	global judgeid
	global laquestion
	global selection
	global selectId
	global Players
	global joueurgagnant
	global Number_Of_Players

	selection = []
	user = request.form['username']								#va chercher le username de l'utilisateur
	choix = int(request.form['choix'])							#va chercher le choix de l'utilisateur

	if(user == judgeid):										#si le joueur est le juge
		joueurgagnant = selectId[choix-1]						#son choix est le joueur gagnant
		index_Prompts = index_Prompts + 1
		laquestion = Prompts[index_Prompts][0]
	
	temp = Players[random.randrange(Number_Of_Players)].Id		#établie un nouveau juge
	while (temp == judgeid):									#si le nouveau juge est différent
		temp = Players[random.randrange(Number_Of_Players)].Id
	
	judgeid = temp

	return render_template("formulairegagnant.html", winner = joueurgagnant, user = user)

if __name__ == '__main__':

	ni.ifaddresses('eth0')
	ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

	os.system("sudo chmod 777 /sys/jalon3ecran/ecran/ecran")	#affiche sur le lcd du BBB
	f = open("/sys/jalon3ecran/ecran/ecran", "w")
	f.write(ip + ":5000")
	f.close()

	app.run(host = ip, port = 5000)
