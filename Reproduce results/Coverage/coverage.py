from tkinter import * 
import csv
import pandas as pd
import re
import pickle
   
INPUT_PATH = './verification.txt'
DICT_PATH = './subevent.pkl'
_nonbmp = re.compile(r'[\U00010000-\U0010FFFF]')


''' 
------------------------------------------------------------------------
Uncomment to re-initialize the file

df_input = pd.read_csv(INPUT_PATH)
df_input["vu"] = False
df_input["new"] = False
df_input.to_csv(OUTPUT_PATH,index=False)
-------------------------------------------------------------------------
'''

d_subevent = pickle.load( open( DICT_PATH, "rb" ) )
subevent_pre = []
id_me_pred = []

def not_at_all():
	global event
	global id_me
	global texte
	global id_me_pred
	global subevent
	global subevent_pre
	subevent_pre.append(subevent)
	id_me_pred.append(id_me)
	df_output.at[df_output[df_output["id"]==id_me].index.values.astype(int)[0],subevent] = "Not at all"
	event, id_me, texte, texte2, subevent = init2()
	c1.itemconfigure(textc1,text=texte)
	c2.itemconfigure(textc2,text=texte2)
	return 0

def partly():
	global event
	global id_me
	global texte
	global id_me_pred
	global subevent
	global subevent_pre
	subevent_pre.append(subevent)
	id_me_pred.append(id_me)
	df_output.at[df_output[df_output["id"]==id_me].index.values.astype(int)[0],subevent] = "Partly"
	event, id_me, texte, texte2, subevent = init2()
	c1.itemconfigure(textc1,text=texte)
	c2.itemconfigure(textc2,text=texte2)
	return 0

def the_whole():
	global event
	global id_me
	global texte
	global id_me_pred
	global df_output
	global subevent
	global subevent_pre
	subevent_pre.append(subevent)
	id_me_pred.append(id_me)
	df_output.at[df_output[df_output["id"]==id_me].index.values.astype(int)[0],subevent] = "The whole"
	event, id_me, texte, texte2, subevent = init2()
	c1.itemconfigure(textc1,text=texte)
	c2.itemconfigure(textc2,text=texte2)
	return 0

def undo():
	global event
	global id_me
	global texte
	global id_me_pred
	global df_output
	global subevent
	global subevent_pre
	if subevent_pre:
		df_output.at[df_output[df_output["id"]==id_me_pred[-1]].index.values.astype(int)[0],subevent_pre[-1]] = "Not yet assessed"
		subevent_pre.pop()
		id_me_pred.pop()
		event, id_me, texte, texte2, subevent = init2()
		c1.itemconfigure(textc1,text=texte)
		c2.itemconfigure(textc2,text=texte2)
	return 0

def init():
	df_output = pd.read_csv(INPUT_PATH)
	return df_output
	
def on_closing():
	df_output.to_csv(INPUT_PATH,index=False)
	fenetre.destroy()

df_output = init()

fenetre = Tk()

def _surrogatepair(match):
    char = match.group()
    assert ord(char) > 0xffff
    encoded = char.encode('utf-16-le')
    return (
        chr(int.from_bytes(encoded[:2], 'little')) + 
        chr(int.from_bytes(encoded[2:], 'little')))

def with_surrogates(text):
    return _nonbmp.sub(_surrogatepair, text)

def already_assessed(df_output,i_row):
	for i in d_subevent:
		if df_output[i][i_row] == "Not yet assessed":
			return False
	return True

def init2():
	for i in range(len(df_output["assessed"])):
		if df_output["assessed"][i] == False:
			if already_assessed(df_output,i):
				df_output.at[i,"assessed"] = True

	event = list(df_output[df_output["assessed"]==False]["content.event"])[0]
	id_me = list(df_output[df_output["assessed"]==False]["id"])[0]
	for i in d_subevent:
		if df_output[i][df_output[df_output["id"]==id_me].index.values.astype(int)[0]] == "Not yet assessed":
			subevent = i
			break

	texte = str(event) + "\n" + str(df_output[df_output["id"]==id_me].index.values.astype(int)[0]) + " "
	for i in df_output[df_output["id"]==id_me]["content.text"]:
		texte+=i
	texte=with_surrogates(texte)

	texte2 = d_subevent[subevent]

	texte2 = with_surrogates(texte2)

	return event, id_me, texte, texte2, subevent

event, id_me, texte, texte2, subevent = init2()

c1 = Canvas(fenetre, width=500, height=500, bg='ivory')

scroll_x = Scrollbar(fenetre, orient="horizontal", command=c1.xview)
scroll_x.pack(side=BOTTOM, padx=5, pady=5)
scroll_y = Scrollbar(fenetre, orient="vertical", command=c1.yview)
scroll_y.pack(side=LEFT, padx=5, pady=5)
c1.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
c1.pack(side=LEFT, padx=5, pady=5)
textc1 = c1.create_text(500,500,fill="black",font="Helvetica 10", text=texte, width=500, anchor='se')

choice1 = Button(fenetre, text ='Not at all',bg='red',width=6,height=2,command=lambda : not_at_all()).place(x=560, y=350)
choice2 = Button(fenetre, text ='Partly',bg='orange',width=6,height=2,command=lambda : partly()).place(x=650, y=350)
choice3 = Button(fenetre, text ='The whole',bg='green',width=6,height=2,command=lambda : the_whole()).place(x=740, y=350)
choice4 = Button(fenetre, text ='Undo',bg='white',width=6,height=2,command=lambda : undo()).place(x=650, y=60)

c2 = Canvas(fenetre, width=300, height=200, bg='ivory')
scroll_x2 = Scrollbar(fenetre, orient="horizontal", command=c2.xview)
scroll_x2.pack(side=BOTTOM, padx=5, pady=5)
scroll_y2 = Scrollbar(fenetre, orient="vertical", command=c2.yview)
scroll_y2.pack(side=LEFT, padx=5, pady=5)
c2.configure(yscrollcommand=scroll_y2.set, xscrollcommand=scroll_x2.set)
c2.pack(side=LEFT, padx=5, pady=5)
textc2 = c2.create_text(300,200,fill="black",font="Helvetica 10", text=texte2, width=300, anchor='se')

fenetre.protocol("WM_DELETE_WINDOW", on_closing)
fenetre.mainloop()