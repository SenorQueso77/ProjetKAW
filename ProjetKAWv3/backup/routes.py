from KAW import KAW
from flask import Flask,request,render_template

import os

#app = Flask(__name__)

main1 = ["A lifetime of sadness","Tastefull sideboob","Men","Gandhi","A zesty breakfast burrito"]
main2 = ["A fully dressed female videogame character","Sharing needles","Grandpa's ashes","A windmill full of corpses","Michael Jackson"]
laquestion = "what do old people smell like?"
judgeid =1
firstid =2
secondid =3

@KAW.route('/')
@KAW.route('/kaw_tour', methods=['POST'])
def kawturn():
	global judgeid
	global firstid
	global secondid
	global main1
	global main2
	global laquestion
	#judgeid = 1
	#laquestion = "what do old people smell like?"
	#firstid = 2
	#secondid = 3
	#main1 = ["A lifetime of sadness","Tastefull sideboob","Men","Gandhi","A zesty breakfast burrito"]
	#main2 = ["A fully dressed female videogame character","Sharing needles","Grandpa's ashes","A windmill full of corpses","Michael Jackson"]

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

#if __name__== "__main__":
#	app.run(host='192.168.2.3', port=80)

