#!/usr/bin/env python
# coding: utf-8

""" 
    LTAT.01.003 Tehisintellekt (2017 sügis)
    Kodutöö nr 7. "Music chatbot"

    Autor: Jan Moppel 
    
"""

# Fail, millest käivitatakse dialoogsüsteem konsooliaknas

import chat_ai
import bot_trainer


print("Bot: Hi, I am a music helper bot.")

# Juturoboti treenimine. Võtab päris palju aega (30min +).
bot_trainer.train()

while True:
    human = input("User: ")
    # Programmi töö lõpetamine, kui kasutaja kirjutab "bye"
    if human == "bye":
        print("Bot: Dialog is over.")
        break
    # Arvuti vastus lausele
    print("Bot: ", chat_ai.getResponse(human))

