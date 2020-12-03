from tkinter import * 
import csv
import pandas as pd
import re
   
INPUT_PATH = './input.txt'
OUTPUT_PATH = './output.txt'
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

def initialize():
	df_input = pd.read_csv(INPUT_PATH)
	df_input["vu"] = False
	df_input["new"] = False
	df_input.to_csv(OUTPUT_PATH,index=False)
	return df_summary

def new():
	global event
	global id_me
	global texte
	global id_me_pred
	df_output.loc[df_output["id"]==id_me,["new"]]=True
	df_output.loc[df_output["id"]==id_me,["vu"]]=True
	event, id_me, texte, texte2, id_me_pred = init2()
	c1.itemconfigure(textc1,text=texte)
	c2.itemconfigure(textc2,text=texte2)
	return 0

def already_known():
	global event
	global id_me
	global texte
	global id_me_pred
	df_output.loc[df_output["id"]==id_me,["new"]]=False
	df_output.loc[df_output["id"]==id_me,["vu"]]=True
	event, id_me, texte, texte2, id_me_pred = init2()
	c1.itemconfigure(textc1,text=texte)
	c2.itemconfigure(textc2,text=texte2)
	return 0

def undo():
	global event
	global id_me
	global texte
	global id_me_pred
	global df_output
	df_output.loc[df_output["id"]==id_me_pred,["new"]]=False
	df_output.loc[df_output["id"]==id_me_pred,["vu"]]=False
	event, id_me, texte, texte2, id_me_pred = init2()
	c1.itemconfigure(textc1,text=texte)
	c2.itemconfigure(textc2,text=texte2)
	return 0

def init():
	df_output = pd.read_csv(OUTPUT_PATH)
	return df_output
	
def on_closing():
	df_output.to_csv(OUTPUT_PATH,index=False)
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

def init2():
	event = list(df_output[df_output["vu"]==False]["content.event"])[0]
	id_me = list(df_output[df_output["vu"]==False]["id"])[0]
	try:
		id_me_pred = list(df_output[df_output["vu"]==True]["id"])[-1]
	except:
		id_me_pred = id_me

	texte = ""

	df_transi = df_output[(df_output["content.event"]==event)]
	for i in df_transi[df_transi["new"]==True]["content.text"]:
		texte+=i+"\n"
	texte=with_surrogates(texte)

	texte2 = str(event) + "\n" + str(df_output[df_output["id"]==id_me].index.values.astype(int)[0]) + " "
	for i in df_output[df_output["id"]==id_me]["content.text"]:
		texte2+=i
	texte2=with_surrogates(texte2)

	return event, id_me, texte, texte2, id_me_pred

event, id_me, texte, texte2, id_me_pred = init2()

c1 = Canvas(fenetre, width=500, height=500, bg='ivory')

scroll_x = Scrollbar(fenetre, orient="horizontal", command=c1.xview)
scroll_x.pack(side=BOTTOM, padx=5, pady=5)
scroll_y = Scrollbar(fenetre, orient="vertical", command=c1.yview)
scroll_y.pack(side=LEFT, padx=5, pady=5)
c1.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
c1.pack(side=LEFT, padx=5, pady=5)
textc1 = c1.create_text(500,500,fill="black",font="Helvetica 10", text=texte, width=500, anchor='se')

choice1 = Button(fenetre, text ='New',bg='green',command=lambda : new()).pack(side=LEFT, padx=5, pady=5)
choice2 = Button(fenetre, text ='Already known',bg='red',command=lambda : already_known()).pack(side=RIGHT, padx=5, pady=5)
choice3 = Button(fenetre, text ='Undo',bg='white',command=lambda : undo()).pack(side=TOP, padx=5, pady=5)

c2 = Canvas(fenetre, width=200, height=100, bg='ivory')
scroll_x2 = Scrollbar(fenetre, orient="horizontal", command=c2.xview)
scroll_x2.pack(side=BOTTOM, padx=5, pady=5)
scroll_y2 = Scrollbar(fenetre, orient="vertical", command=c2.yview)
scroll_y2.pack(side=LEFT, padx=5, pady=5)
c2.configure(yscrollcommand=scroll_y2.set, xscrollcommand=scroll_x2.set)
c2.pack(side=LEFT, padx=5, pady=5)
textc2 = c2.create_text(200,100,fill="black",font="Helvetica 10", text=texte2, width=200, anchor='se')

fenetre.protocol("WM_DELETE_WINDOW", on_closing)
fenetre.mainloop()
