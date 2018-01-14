#!/usr/bin/env python
# coding: utf-8

""" 
    LTAT.01.003 Tehisintellekt (2017 sügis)
    Kodutöö nr 7. "Music chatbot"

    Autor: Jan Moppel 
    
"""


# Graafiline kasutajaliides
# Fail, millest käivitatakse dialoogsüsteem graafilises vaates

import chat_ai
import bot_trainer
from tkinter import *


def saadaDialoogi():
    global tkTurnNr
    human = user.get()
    dialogueList.insert(END, "User: " + human+'\n')
#    dialogueList.itemconfig(tkTurnNr*2-1, {'bg':tkColor2})
    if human == "bye":
        dialogueList.insert(END, "Bot: Dialog is over.", 'bot')
 #       dialogueList.itemconfig(tkTurnNr*2, {'bg':tkColor1})
        finish()
        return
    dialogueList.insert(END, "Bot: " + str(chat_ai.getResponse(human))+'\n', 'bot')
    dialogueList.yview(END)
  #  dialogueList.itemconfig(tkTurnNr*2, {'bg':tkColor1})
    userInput.set("")
    user.focus()
    tkTurnNr += 1

def sendEnter(event):
    if endDial == False:
        saadaDialoogi()

def finish():
    global endDial
    endDial = True
    user.configure(state="disabled")
    button.configure(state="disabled")

# Juturoboti treenimine. Võtab päris palju aega (30min +).
bot_trainer.train()

# Disain
tkColor1 = 'light sky blue'
tkColor2 = 'White'
tkColor3 = 'midnight blue'
tkTurnNr = 1
tkDialogueWidth = 120
tkDialogueHeight = 30

endDial = False

# Akna loomine
root = Tk()
root.wm_title("Music Helper")
root.configure(background=tkColor2)

# Pealkiri
title = Label(root, text="Music Helper", fg=tkColor3, font=("Helvetica", 20), background=tkColor2)

# Dialoogi listi loomine
"""dialogueList = Listbox(root, width=tkDialogueWidth, height=tkDialogueHeight)
dialogueList.insert(END, "Bot: Hi, I am a music helper bot.")
dialogueList.itemconfig(0, {'bg':tkColor1})"""
dialogueList = Text(root, width=tkDialogueWidth, height=tkDialogueHeight)
dialogueList.tag_configure('bot', foreground='#609732')
dialogueList.insert(END, "Bot: Hi, I am a music helper bot.\n", 'bot')

# Saatmisnupu loomine
button = Button(root, text ="Send!", command = saadaDialoogi)

# Vastuselahtri loomine
userInput = StringVar()
user = Entry(root, textvariable = userInput, width=150)
user.focus()
# Saatmiseks piisab ka Enter-klahvi vajutusest
root.bind('<Return>', sendEnter)

title.pack(fill=X, padx=10, pady=10)
dialogueList.pack(fill=X, padx=10, pady=10)
user.pack(side=LEFT, fill=X, padx=10, pady=10)
button.pack(side=RIGHT, fill=X, padx=10, pady=10)

# Tsükkel, mis hoiab akna avatuna
root.mainloop()




