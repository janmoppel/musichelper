#!/usr/bin/env python
# coding: utf-8

""" 
    LTAT.01.003 Tehisintellekt (2017 sügis)
    Kodutöö nr 7. "Music chatbot"

    Autor: Jan Moppel 

"""

# Treenimisfail. Siia võib lisada lauseid treenimiseks

import sys, os

# Make sure you put the mitielib folder into the python search path.  There are
# a lot of ways to do this, here we do it programmatically with the following
# two statements:
parent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(parent + '/../../mitielib')
from mitie import *
import nltk


# Lisame uusi entities
def entities(trainer):
    samples = []

    sample1 = ner_training_instance(["I", "like", "Post", "Malone"])
    sample1.add_entity(xrange(2, 4), "artist")
    samples.append(sample1)

    sample2 = ner_training_instance(['I', 'like', 'rock-music'])
    sample2.add_entity(xrange(2, 3), "tag")
    samples.append(sample2)

    sample3 = ner_training_instance(['I', 'like', 'rock', 'music'])
    sample3.add_entity(xrange(2, 3), "tag")
    samples.append(sample3)

    sample4 = ner_training_instance(['I', 'like', 'rock', 'genre'])
    sample4.add_entity(xrange(2, 3), "tag")
    samples.append(sample4)

    sample5 = ner_training_instance(['I', 'like', 'pop'])
    sample5.add_entity(xrange(2, 3), "tag")
    samples.append(sample5)

    sample6 = ner_training_instance(["I", "like", "G-Eazy"])
    sample6.add_entity(xrange(2, 3), "artist")
    samples.append(sample6)

    sample7 = ner_training_instance(['I', 'like', 'Rock-music'])
    sample7.add_entity(xrange(2, 3), "tag")
    samples.append(sample7)

    sample8 = ner_training_instance(['I', 'like', 'Rock', 'music'])
    sample8.add_entity(xrange(2, 3), "tag")
    samples.append(sample8)

    sample9 = ner_training_instance(['I', 'like', 'Rock', 'genre'])
    sample9.add_entity(xrange(2, 3), "tag")
    samples.append(sample9)

    sample10 = ner_training_instance(['I', 'like', 'Pop'])
    sample10.add_entity(xrange(2, 3), "tag")
    samples.append(sample10)

    sample11 = ner_training_instance(['Recommend', 'me', 'something', 'from', 'pop'])
    sample11.add_entity(xrange(4, 5), "tag")
    samples.append(sample11)

    sample12 = ner_training_instance(['Recommend', 'me', 'something', 'from', 'Pop'])
    sample12.add_entity(xrange(4, 5), "tag")
    samples.append(sample12)

    sample13 = ner_training_instance(['Recommend', 'me', 'something', 'from', 'pop', 'genre'])
    sample13.add_entity(xrange(4, 5), "tag")
    samples.append(sample13)

    sample14 = ner_training_instance(['Recommend', 'me', 'something', 'from', 'Pop', 'genre'])
    sample14.add_entity(xrange(4, 5), "tag")
    samples.append(sample14)

    sample15 = ner_training_instance(['Recommend', 'some', 'artists', 'like', 'Led', 'Zeppelin'])
    sample15.add_entity(xrange(4, 6), "artist")
    samples.append(sample15)

    sample16 = ner_training_instance(['Recommend', 'something', 'from', 'popular', 'music'])
    sample16.add_entity(xrange(3, 4), "tag")
    samples.append(sample16)

    sample17 = ner_training_instance(['Recommend', 'something', 'from', 'Popular', 'music'])
    sample17.add_entity(xrange(3, 4), "tag")
    samples.append(sample17)

    sample18 = ner_training_instance(['Recommend', 'a', 'song', 'like', '``', 'Stairway', 'to', 'Heaven', "''"])
    sample18.add_entity(xrange(5, 8), "song")
    samples.append(sample18)

    sample19 = ner_training_instance(['What', 'are', '``', 'Stairway', 'to', 'Heaven', "''", 'words'])
    sample19.add_entity(xrange(3, 6), "song")
    samples.append(sample19)

    sample20 = ner_training_instance(['Who', 'is', 'the', 'author', 'of', '``', 'Shape', 'of', 'you', "''"])
    sample20.add_entity(xrange(6, 9), "song")
    samples.append(sample20)

    sample21 = ner_training_instance(['``', 'Shape', 'of', 'you', "''", 'is', 'Ed', 'Sheeran', "'s", 'song'])
    sample21.add_entity(xrange(1, 4), "song")
    sample21.add_entity(xrange(5, 7), "artist")
    samples.append(sample21)

    sample22 = ner_training_instance(['When', 'the', 'album', '``', 'Queen', 'II', "''", 'was', 'recorded'])
    sample22.add_entity(xrange(4, 6), "album")
    samples.append(sample22)

    sample23 = ner_training_instance(['What', 'songs', 'were', 'on', 'the', 'album', '``', 'Queen', 'II', "''"])
    sample23.add_entity(xrange(7, 9), "album")
    samples.append(sample23)

    sample24 = ner_training_instance(['Recommend', 'me', 'songs', 'like', '``', 'Help', "''"])
    sample24.add_entity(xrange(5, 6), "song")
    samples.append(sample24)

    sample25 = ner_training_instance(['Recommend', 'me', 'artists', 'like', 'Frank', 'Sinatra'])
    sample25.add_entity(xrange(4, 6), "artist")
    samples.append(sample25)

    sample26 = ner_training_instance(['When', 'was', 'the', 'album', '``', 'Dire', 'Straits', "''", 'written', '?'])
    sample26.add_entity(xrange(5, 7), "album")
    samples.append(sample26)

    sample27 = ner_training_instance(['``', 'Since', 'I', "'ve", 'been', 'loving', 'you', "''", 'is', 'Led', 'Zeppelin', "'s", 'song', '?'])
    sample27.add_entity(xrange(1, 7), "song")
    sample27.add_entity(xrange(9, 11), "artist")
    samples.append(sample27)

    sample28 = ner_training_instance(['Can', 'you', 'please', 'recommend', 'me', 'some', 'songs', 'by', 'Din', 'Martin', '?'])
    sample28.add_entity(xrange(8, 10), "artist")
    samples.append(sample28)

    sample29 = ner_training_instance(['Recommend', 'me', 'some', 'musicians', 'like', 'Frank', 'Sinatra'])
    sample29.add_entity(xrange(5, 7), "artist")
    samples.append(sample29)

    sample30 = ner_training_instance(['When', 'did', 'the', 'song', '``', 'Yellow', "''", 'by', 'Coldplay', 'come', 'out', '?'])
    sample30.add_entity(xrange(5, 6), "song")
    sample30.add_entity(xrange(8, 9), "artist")
    samples.append(sample30)

    sample31 = ner_training_instance(['Who', 'wrote', 'the', 'song', '``', 'Yellow', "''", '?'])
    sample31.add_entity(xrange(5, 6), "song")
    samples.append(sample31)

    sample32 = ner_training_instance(['Recommend', 'me', 'some', 'Post-Rock', 'songs'])
    sample32.add_entity(xrange(3, 4), "tag")
    samples.append(sample32)

    sample33 = ner_training_instance(['Information', 'about', 'the', 'album', '``', 'Dire', 'Straits', "''"])
    sample33.add_entity(xrange(5, 7), "album")
    samples.append(sample33)

    sample34 = ner_training_instance(['Give', 'me', 'information', 'about', 'the', 'album', '``', 'Dire', 'Straits', "''"])
    sample34.add_entity(xrange(7, 9), "album")
    samples.append(sample34)

    sample35 = ner_training_instance(['When', 'was', 'the', 'album', '``', 'Dire', 'Straits', "''", 'written', '?'])
    sample35.add_entity(xrange(5, 7), "album")
    samples.append(sample35)

    sample36 = ner_training_instance(['When', 'was', 'the', 'song', '``', 'Unchain', 'my', 'heart', "''", 'written', '?'])
    sample36.add_entity(xrange(5, 8), "song")
    samples.append(sample36)

    sample37 = ner_training_instance(['When', 'was', 'the', 'song', '``', 'Unchain', 'my', 'Heart', "''", 'written', '?'])
    sample37.add_entity(xrange(5, 8), "song")
    samples.append(sample37)

    sample38 = ner_training_instance(['When', 'was', 'the', 'song', '``', 'Unchain', 'My', 'Heart', "''", 'written', '?'])
    sample38.add_entity(xrange(5, 8), "song")
    samples.append(sample38)

    sample39 = ner_training_instance(['``', 'Since', 'I', "'ve", 'been', 'loving', 'you', "''", 'is', 'Led', 'Zeppelin', "'s", 'song', '?'])
    sample39.add_entity(xrange(1, 7), "song")
    sample39.add_entity(xrange(9, 11), "artist")
    samples.append(sample39)

    sample40 = ner_training_instance(
        ['``', 'Since', 'I', "'ve", 'been', 'loving', 'You', "''", 'is', 'Led', 'Zeppelin', "'s", 'song', '?'])
    sample40.add_entity(xrange(1, 7), "song")
    sample40.add_entity(xrange(9, 11), "artist")
    samples.append(sample40)

    sample41 = ner_training_instance(
        ['``', 'Since', 'I', "'ve", 'been', 'Loving', 'You', "''", 'is', 'Led', 'Zeppelin', "'s", 'song', '?'])
    sample41.add_entity(xrange(1, 7), "song")
    sample41.add_entity(xrange(9, 11), "artist")
    samples.append(sample41)

    sample42 = ner_training_instance(
        ['``', 'Since', 'I', "'ve", 'Been', 'Loving', 'You', "''", 'is', 'Led', 'Zeppelin', "'s", 'song', '?'])
    sample42.add_entity(xrange(1, 7), "song")
    sample42.add_entity(xrange(9, 11), "artist")
    samples.append(sample42)

    sample43 = ner_training_instance(
        ['``', 'Since', 'I', "'ve", 'been', 'Loving', 'you', "''", 'is', 'Led', 'Zeppelin', "'s", 'song', '?'])
    sample43.add_entity(xrange(1, 7), "song")
    sample43.add_entity(xrange(9, 11), "artist")
    samples.append(sample43)

    sample44 = ner_training_instance(
        ['``', 'Since', 'I', "'ve", 'Been', 'loving', 'you', "''", 'is', 'Led', 'Zeppelin', "'s", 'song', '?'])
    sample44.add_entity(xrange(1, 7), "song")
    sample44.add_entity(xrange(9, 11), "artist")
    samples.append(sample44)

    sample45 = ner_training_instance(
        ['``', 'Since', 'I', "'ve", 'Been', 'loving', 'You', "''", 'is', 'Led', 'Zeppelin', "'s", 'song', '?'])
    sample45.add_entity(xrange(1, 7), "song")
    sample45.add_entity(xrange(9, 11), "artist")
    samples.append(sample45)

    sample46 = ner_training_instance(
        ['``', 'Since', 'I', "'ve", 'Been', 'Loving', 'you', "''", 'is', 'Led', 'Zeppelin', "'s", 'song', '?'])
    sample46.add_entity(xrange(1, 7), "song")
    sample46.add_entity(xrange(9, 11), "artist")
    samples.append(sample46)

    sample47 = ner_training_instance(
        ['Give', 'me', 'an', 'information', 'about', '``', 'Stairway', 'to', 'Heaven', "''"])
    sample47.add_entity(xrange(6, 9), "song")
    samples.append(sample47)

    sample48 = ner_training_instance(
        ['Provide', 'me', 'some', 'information', 'about', 'The', 'Jimi', 'Hendrix', 'Experience'])
    sample48.add_entity(xrange(5, 9), "artist")
    samples.append(sample48)

    sample49 = ner_training_instance(
        ['Provide', 'me', 'information', 'about', 'Ed', 'Sheeran'])
    sample49.add_entity(xrange(4, 6), "artist")
    samples.append(sample49)

    sample50 = ner_training_instance(
        ['Give', 'me', 'information', 'about', 'Ed', 'Sheeran'])
    sample50.add_entity(xrange(4, 6), "artist")
    samples.append(sample50)

    sample51 = ner_training_instance(
        ['Give', 'me', 'info', 'about', 'Ed', 'Sheeran'])
    sample51.add_entity(xrange(4, 6), "artist")
    samples.append(sample51)

    sample52 = ner_training_instance(
        ['Some', 'info', 'about', 'Ed', 'Sheeran'])
    sample52.add_entity(xrange(3, 5), "artist")
    samples.append(sample52)

    sample53 = ner_training_instance(
        ['Some', 'information', 'about', 'Ed', 'Sheeran'])
    sample53.add_entity(xrange(3, 5), "artist")
    samples.append(sample53)

    for sample in samples:
        trainer.add(sample)

    return


def train():
    # Text categorizer
    trainer = text_categorizer_trainer("../../MITIE-models/english/total_word_feature_extractor.dat")

    # Meie treenimise data
    data = {
        "greet": {
            "examples": ["hello", "hey there", "howdy", "hello", "hi", "hey", "hey ho", "yo", "what's up"],
            "centroid": None
        },
        "help": {
            "examples": [
                "what are you able to do",
                "what are your abilities",
                "what can you do"
            ],
            "centroid": None
        },
        "songs": {
            "examples": [
                "recommend some music to listen",  # --
                "can you please find me some music to listen",  # --
                "recommend me songs like \"Help\"",
                "Can you please recommend me some songs by Din Martin'",
                "i like rock-music",  # rock-music - person
                "i like rock music",  # Rock music - person
                "i like rock genre",  # Rock genre - person
                "i like pop",  # Pop - person
                "recommend me something from pop",  # pop - organization
                "recommend me something from pop genre",  # Pop - organization
                "recommend something from popular music",  # Popular - organization
                "Recommend me some Post-Rock songs",
                "What's the most trending song right now",
                "What's the most popular song right now",
                "recommend a song like \"Stairway to Heaven\"",  # " Stairway - person; # to Heaven - person
                "i like Post Malone",   # end
                "Recommend me some songs by Frank Sinatra",
                "Recommend me something from Frank Sinatra",
                "Now recommend me some music to listen to"
            ],
            "centroid": None
        },
        "artists": {
            "examples": [
                "recommend me artists like Frank Sinatra",
                "recommend me some musicians like Frank Sinatra",
                "recommend some artists like Led Zeppelin",
                "who is the author of \"Shape of you\""
            ],
            "centroid": None
        },
        "info": {
            "examples": [
                "When did the song \"Yellow\" by Coldplay come out?",
                "Information about the album \"Dire Straits\"",
                "Give me information about the album \"Dire Straits\"",
                "when was the album \"Dire Straits\" written",
                "when was the song \"Unchain my heart\" written",
                "when was the song \"Unchain my Heart\" written",
                "when was the song \"Unchain My Heart\" written",
                "\"Since I've been loving you\" is Led Zeppelin's song",
                "Give me an information about \"Stairway to Heaven\"",
                "Provide me some information about The Jimi Hendrix Experience",
                "\"Shape of you\" is Ed Sheeran's song",
                "when the album \"Queen II\" was recorded",
                "Who wrote the song \"Yellow\"",
                "what songs were on the album \"Queen II\"",
                "\"Since I've been loving You\" is Led Zeppelin's song",
                "\"Since I've been Loving You\" is Led Zeppelin's song",
                "\"Since I've Been Loving You\" is Led Zeppelin's song",
                "\"Since I've Been loving You\" is Led Zeppelin's song",
                "\"Since I've Been loving you\" is Led Zeppelin's song",
                "\"Since I've Been Loving you\" is Led Zeppelin's song",
                "\"Since I've been Loving you\" is Led Zeppelin's song"
            ],
            "centroid": None
        },
        "deny": {
            "examples": [
                "nah",
                "no",
                "not my thing",
                "not my style",
                "i don't like it",
                "i don't enjoy it",
                "recommend something else"
            ],
            "centroid": None
        },
        "accept": {
            "examples": ["thanks", "thank you", "cool, thanks", "cool"],
            "centroid": None
        }
    }

    for label in data.keys():
        for text in data[label]["examples"]:
            tokens = nltk.word_tokenize(text)
            trainer.add_labeled_text(tokens, label)

    # The trainer can take advantage of a multi-core CPU.  So set the number of threads
    # equal to the number of processing cores for maximum training speed.
    trainer.num_threads = 4

    # This function does the work of training.  Note that it can take a long time to run
    # when using larger training datasets.  So be patient.
    cat = trainer.train()

    # Now that training is done we can save the categorizer object to disk like so.  This will
    # allow you to load the model back in using a statement like:
    #   cat = text_categorizer("music_text_categorizer.dat").
    cat.save_to_disk("music_text_categorizer.dat")


    # Named entity recognition
    trainer = ner_trainer("../../MITIE-models/english/total_word_feature_extractor.dat")
    entities(trainer)

    # The trainer can take advantage of a multi-core CPU.  So set the number of threads
    # equal to the number of processing cores for maximum training speed.
    trainer.num_threads = 4

    # This function does the work of training.  Note that it can take a long time to run
    # when using larger training datasets.  So be patient.
    ner = trainer.train()

    # Now that training is done we can save the ner object to disk like so.  This will
    # allow you to load the model back in using a statement like:
    #   ner = named_entity_extractor("music_ner_model.dat").
    ner.save_to_disk("music_ner_model.dat")

    return
