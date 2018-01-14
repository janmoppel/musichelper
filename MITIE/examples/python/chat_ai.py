#!/usr/bin/env python
# coding: utf-8

""" 
    LTAT.01.003 Tehisintellekt (2017 sügis)
    Kodutöö nr 7. "Music chatbot"

    Autor: Jan Moppel 

"""

# Peamine funktsioon on getResponse(),
# millele antakse argumendina ette kasutajalt sisendiks saadud tekst (sõnena)
# ja mis tagastab sobiva vastuse (samuti sõnena).
import urllib.request
import json
import nltk
import random

import sys, os

# Make sure you put the mitielib folder into the python search path.  There are
# a lot of ways to do this, here we do it programmatically with the following
# two statements:
parent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(parent + '/../../mitielib')

from mitie import *

# freim
freim = {'song': [], 'artist': [], 'tag': [], 'album': [], 'task': '00'}

# Text categorizer
cat = text_categorizer("music_text_categorizer.dat")

# Named entity recognition
ner = named_entity_extractor("music_ner_model.dat")  # ("../../MITIE-models/english/ner_model.dat")


def getResponse(text):

    # Respons'i vaikeväärtus
    response = "Sorry, I don't understand you. Can you say it again? " \
               "Although remember, that I'm only a music helper bot :)"

    # NLP töötab tokenizeeritud lausega
    tokens = nltk.word_tokenize(text)
    #print(tokens)

    # Text recognition
    predicted_label, _ = cat(tokens)

    # Named Entity Recognition
    entities = ner.extract_entities(tokens)

    # Siin me kontrollime praegust ülesannet
    task = freim['task']
    # Tulevikus kontrollime mis named entities saime kätte
    updates = [False, False, False, False]  # songs, artists, tags, album

    # Kontrollime, mis ülesanne robotil olemas
    if task[1] == '2':  # Artisti nimi on puudu
        freim['task'] = '00'  # Paneme taski tagasi 0 väärtuseks
        try:
            artist_name = " ".join(tokens[i] for i in entities[0][0])   # Kui oleme siin, siis kasutaja
                                                                        # kirjutas artisti nime
            freim['artist'].append(artist_name)

            if task == '12':  #  Ülesanne - leida samasugusi laule (song +, artist -)
                return getSimilarSongs()
            elif task == '72':  # Leida info albumi kohta
                return getAlbumInfo()
            elif task == '62':  # Leida info laulu kohta
                return getSongInfo()

        except:
            return "Sorry, but I need an artist name to complete this task. So, I cannot help you :("

    # Kui probleemset taski polnud: kasutame tavalist analüüsi
    # Algselt vaatleme teksti kategooriat: greet, help, songs, artists, info, accept, deny
    if predicted_label == "greet":
        response = "How can I help you?"
    elif predicted_label == "help":
        response = "I am a music helper bot. I can find music artists by genres (tags) and your favorite songs/albums etc." \
                   "I also can provide you a brief information about songs, albums, artists."

    # Robot otsib lugusid
    elif predicted_label == "songs":

        # Vaatleme entities, mida meie mudel leidis
        findEntities(entities, updates, tokens)

        # Laul +, artist +
        if updates[0] and updates[1]:
            freim['task'] = '11'   # 1 == find similair song
                                 # 1 == song +, artist +

            response = getSimilarSongs()

        # Laul +, artist -
        elif updates[0]:
            freim['task'] = '12'   # 1 == find similair song
                                 # 2 == song +, artist -
            response = "Do you know what is the artist's name?"

        # Laul -, artist +
        elif updates[1]:
            freim['task'] = '21'  # 2 == find songs of artist
                                # 1 == artist +
            response = getArtistSongs()

        # Laul -, Artist -, Tag +
        elif updates[2]:
            freim['task'] = '31'    # 3 == find songs by tag
                                    # 1 == tag +
            tag = freim['tag'][-1]
            response = getSongsByTag(tag)

        # Robot üritab soovitada uut muusikat selle muusika järgi, mida kasutaja juba ütles
        else:
            freim['task'] = '91'    # 9 == otsida uut muusikat

            # Otsime uut muusikat tagide kaudu

            # Juhul kui info tagi kohta puudub
            if len(freim['tag']) == 0:
                # Otsime taggi artisti kaudu
                if len(freim['artist']) != 0:
                    musician = random.choice(freim['artist'])
                    # Otsime tagge selle artisti järgi
                    if not getTagByArtist(musician):
                        # Ei leidnud taggi selle artisti kohta
                        response = getTopSongs()
            else:
                tag = random.choice(freim['tag'])
                response = getSongsByTag(tag)

    # Robot otsib artiste
    elif predicted_label == "artists":

        # Vaatleme entities, mida meie mudel leidis
        findEntities(entities, updates, tokens)

        # Laul +
        if updates[0]:
            freim['task'] = '41'    # 4 == find artists by songs
                                    # 1 == song +
            response = getArtistBySong()

        # Artist +
        elif updates[1]:
            freim['task'] = '51'    # 5 == find similar artists
                                    # 1 == artist +
            response = getSimilarArtist()
        else:
            response = "I'm sorry, but I couldn't find any information about this artist."

    # Robot otsib üldist informatsiooni
    elif predicted_label == "info":

        # Vaatleme entities, mida meie mudel leidis
        findEntities(entities, updates, tokens)

        # Song +, Artist +
        if updates[0] and updates[1]:
            freim['task'] = '61'  # 6 == get full information about track
                                # 1 == song +, artist +
            response = getSongInfo()

        # Artist +, Album +
        elif updates[1] and updates[3]:
            freim['task'] = '71'  # 7 == get information about album
                                # 1 == album +, artist +
            response = getAlbumInfo()

        # Album +
        elif updates[3]:
            freim['task'] = '72'  # 7 == get information about album
                                # 2 == album +, artist -
            response = "Without artist's name I cannot tell you any information about the album. " \
                       "Do you know what is the artist's name?"

        # Artist +
        elif updates[1]:
            freim['task'] = '81'  # 8 == get information about artist
                                # 1 == artist +
            response = getArtistInfo()

        # Song +
        elif updates[0]:
            freim['task'] = '62'  # 6 == get full information about track
                                # 1 == song +, artist -
            response = "Without artist's name I cannot tell you any information about the track. " \
                       "Do you know what is the artist's name?"

    # Kasutaja on roboti vastusega rahuldatud
    elif predicted_label == "accept":
        freim['task'] = '00'
        response = "You're welcome! Anything else?"

    # Kasutajale ei meeldinud roboti vastust.
    # Nt. robot soovitas kasutajale kuulda artisti, mida kasutajale ei meeldi
    else:   # predicted_label == "deny"
        # Saame aru, mis taski robot üritas täita
        if task[0] == '1':
            response = getSimilarSongs()
        elif task[0] == '2':
            response = getArtistSongs()
        elif task[0] == '3':
            tag = freim['tag'][-1]
            response = getSongsByTag(tag)
        elif task[0] == '4':
            response = getArtistBySong()
        elif task[0] == '5':
            response = getSimilarArtist()
        elif task[0] == '6':
            response = getSongInfo()
        elif task[0] == '7':
            response = getAlbumInfo()
        elif task[0] == '8':
            response = getArtistInfo()
        elif task[0] == '9':
            # Robot üritab soovitada uut muusikat selle muusika järgi, mida kasutaja juba ütles
            freim['task'] = '91'  # 9 == otsida uut muusikat

            # Otsime uut muusikat tagide kaudu

            # Juhul kui info tagi kohta puudub
            if len(freim['tag']) == 0:
                # Otsime taggi artisti kaudu
                if len(freim['artist']) != 0:
                    musician = random.choice(freim['artist'])
                    # Otsime tagge selle artisti järgi
                    if not getTagByArtist(musician):
                        # Ei leidnud taggi selle artisti kohta
                        response = getTopSongs()
            else:
                tag = random.choice(freim['tag'])
                response = getSongsByTag(tag)

    return response


# Transformeerime json sõnastiku kujule
def getDictFromJson(url):
    # Veebist ilmainfo lugemine
    file = urllib.request.urlopen(url)
    data = json.loads(file.read().decode())
    return data


# Otsime entities meie lauses
def findEntities(entities, updates, tokens):
    for e in entities:
        rng = e[0]  # range
        tag = e[1]
        entity_text = " ".join(tokens[i] for i in rng)

        # Kontrollime, mis info saime
        if tag == 'song':
            updates[0] = True
        elif tag == 'artist':
            updates[1] = True
        else:
            updates[2] = True

        freim[tag].append(entity_text)
    return


# Otsime samasuguseid lugusid
def getSimilarSongs():
    # Viimane lugu freimis on see, mida kasutaja pani viimasena kirja
    song = freim['song'][-1]
    # Viimane artist freimis on see, mida kasutaja pani viimasena kirja
    artist = freim['artist'][-1]

    # Kasutame vajalikku meetodi
    file = urllib.request.urlopen('http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist=' +
                                  urllib.parse.quote(artist) + '&track=' + urllib.parse.quote(song) +
                                  '&api_key=' + urllib.parse.quote(API) + '&format=json')

    # Juhul kui viga ei ole -> jätkame
    try:
        tracks = json.loads(file.read().decode())["similartracks"]["track"]

        # Segame kõik lood
        random.shuffle(tracks)

        # Juhul, kui leidsime mingeid lugusid
        if len(tracks) != 0:
            response = "I'd recommend these 5 songs:\n"
            for i in range(5):
                # Valime lugu
                track = tracks[i]
                response += "- \"" + track["name"] + "\" by " + track["artist"]["name"] + "\n"
            return response
    except:
        pass

    # Kui oleme siin, siis päring vastas veaga või ei leidnud ühtegi lugu
    response = "Sorry, but I couldn't find any similair tracks"
    # Kui robot ei saanud leida sellist laulu, siis kustutame meie "andmebaasist" temast igasugune info
    del freim['artist'][-1]
    del freim['song'][-1]

    return response


# Otsime konkreetse artisti lugusid
def getArtistSongs():
    # Viimane artist freimis on see, mida kasutaja pani viimasena kirja
    artist = freim['artist'][-1]

    # Kasutame vajalikku meetodi
    file = urllib.request.urlopen('http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist=' +
                                  urllib.parse.quote(artist) + '&api_key=' + urllib.parse.quote(API) +
                                  '&format=json')

    # Juhul kui viga ei ole -> jätkame
    try:
        tracks = json.loads(file.read().decode())['toptracks']["track"]

        # Segame kõik lood
        random.shuffle(tracks)

        # Juhul, kui leidsime mingeid lugusid
        if len(tracks) != 0:
            response = "I'd recommend these 5 songs by " + str(artist) + ":\n"
            for i in range(5):
                # Valime lugu
                track = tracks[i]
                response += "- \"" + track["name"] + "\" \n"
            return response
    except:
        pass

    # Kui oleme siin, siis päring vastas veaga või ei leidnud ühtegi lugu
    response = "Sorry, but I couldn't find any tracks by that artist"
    # Kui robot ei saanud leida selle artisti lugusid, siis kustutame meie "andmebaasist" temast igasugune info
    del freim['artist'][-1]

    return response


# Otsime lugusid tagi kaudu
def getSongsByTag(tag):

    # Lihtsalt kontrollime, kas kasutaja tahab populaarseid lugusid leida või mitte
    if tag != 'popular' or tag != 'trending':
        # Kasutaja otsib lugusid konkreetses žanris
        file = urllib.request.urlopen('http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag=' +
                                      urllib.parse.quote(tag) + '&api_key=' + urllib.parse.quote(API) +
                                      '&format=json')
    else:
        # Kasutaja otsib populaarseid lugusid
        file = urllib.request.urlopen('http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key=' +
                                      urllib.parse.quote(API) + '&format=json')

    # Juhul kui viga ei ole -> jätkame
    try:
        tracks = json.loads(file.read().decode())['tracks']["track"]

        # Segame kõik lood
        random.shuffle(tracks)

        # Juhul, kui leidsime mingeid lugusid
        if len(tracks) != 0:
            response = "I'd recommend these 5 songs from " + str(tag) + " category:\n"
            for i in range(5):
                # Valime lugu
                track = tracks[i]
                response += "- \"" + track["name"] + "\" by " + track["artist"]["name"] + "\n"
            return response
    except:
        pass

    # Kui oleme siin, siis päring vastas veaga või ei leidnud ühtegi lugu
    response = "Sorry, but I couldn't find any tracks by that tag"
    # Kui robot ei saanud leida selle tagi korral ühtegi laulu laulu,
    # siis kustutame meie "andmebaasist" temast igasugune info
    del freim['tag'][-1]

    return response


# Otsime artiste loo kaudu
def getArtistBySong():
    # Viimane lugu freimis on see, mida kasutaja pani viimasena kirja
    song = freim['song'][-1]

    # Kasutame vajalikku meetodi
    file = urllib.request.urlopen('http://ws.audioscrobbler.com/2.0/?method=track.search&track=' +
                                  urllib.parse.quote(song) + '&api_key=' + urllib.parse.quote(API) +
                                  '&format=json')

    # Juhul kui viga ei ole -> jätkame
    try:
        tracks = json.loads(file.read().decode())['results']["trackmatches"]['track']

        # Juhul, kui leidsime mingeid lugusid
        if len(tracks) != 0:
            response = "I could find these " + str(len(tracks)) + " artists, who wrote song with the title " + \
                       str(song) + ":\n"
            for i in range(len(tracks)):
                # Valime lugu
                track = tracks[i]
                response += "- \"" + track["artist"] + "\" \n"
            return response
    except:
        pass

    # Kui oleme siin, siis päring vastas veaga või ei leidnud ühtegi artisti
    response = "Sorry, but I couldn't find an author of that track"
    # Kui robot ei saanud leida artisti selle lugu kaudu, siis kustutame meie "andmebaasist" loost igasugune info
    del freim['song'][-1]

    return response


# Otsime samasuguseid artiste
def getSimilarArtist():
    # Viimane artist freimis on see, mida kasutaja pani viimasena kirja
    artist = freim['artist'][-1]

    # Kasutame vajalikku meetodi
    file = urllib.request.urlopen('http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist=' +
                                  urllib.parse.quote(artist) + '&api_key=' + urllib.parse.quote(API) +
                                  '&format=json')

    # Juhul kui viga ei ole -> jätkame
    try:
        artists = json.loads(file.read().decode())['similarartists']['artist']

        # Segame kõik artistid
        random.shuffle(artists)

        # Juhul, kui leidsime mingeid artiste
        if len(artists) != 0:
            response = "Check out these 5 artists similar to " + str(artist) + ":\n"
            for i in range(5):
                # Valime muusikut
                musician = artists[i]
                response += "- " + musician["artist"] + "\n"
            return response
    except:
        pass

    # Kui oleme siin, siis päring vastas veaga või ei leidnud ühtegi artisti
    response = "Sorry, but I couldn't find any similar artists"
    # Kui robot ei saanud leida samasuguseid artiste, siis kustutame meie "andmebaasist" temast igasugune info
    del freim['artist'][-1]

    return response


# Otsime informatsiooni loo kohta
def getSongInfo():
    song = freim['song'][-1]
    artist = freim['artist'][-1]

    file = urllib.request.urlopen('http://ws.audioscrobbler.com/2.0/?method=track.getInfo&artist=' +
                                  urllib.parse.quote(artist) + '&track=' + urllib.parse.quote(song) +
                                  '&api_key=' + urllib.parse.quote(API) + '&format=json')
    try:
        track = json.loads(file.read().decode())["track"]

        if len(track) != 0:
            album = track["album"]
            response = "Here's a brief information about this track:\n"
            response += "\"" + track["name"] + "\" by " + track["artist"]["name"] + " appeared on the album " +\
                        album["title"] + "\n"
            response += track["wiki"]["summary"]
            return response
    except:
        pass

    response = "Sorry, but I couldn't find any information about this track"
    # Kui robot ei saanud leida sellist laulu, siis kustutame meie "andmebaasist" temast igasugune info
    del freim['artist'][-1]
    del freim['song'][-1]

    return response


# Otsime informatsiooni albumi kohta
def getAlbumInfo():

    album = freim['album'][-1]
    artist = freim['artist'][-1]

    file = urllib.request.urlopen('http://ws.audioscrobbler.com/2.0/?method=album.getinfo&artist=' +
                                  urllib.parse.quote(artist) + '&album=' + urllib.parse.quote(album) +
                                  '&api_key=' + urllib.parse.quote(API) + '&format=json')
    try:
        album_dict = json.loads(file.read().decode())["album"]

        if len(album_dict) != 0:
            response = "Here's a brief information about this album:\n"
            response += "The album \"" + album_dict["name"] + "\" was written by " + album_dict["artist"] + "\n"
            response += album_dict["wiki"]["summary"]
            return response
    except:
        pass

    response = "Sorry, but I couldn't find any information about this album"
    # Kui robot ei saanud leida sellist albumi, siis kustutame meie "andmebaasist" temast igasugune info
    del freim['artist'][-1]
    del freim['album'][-1]

    return response


# Otsime informatsiooni artisti kohta
def getArtistInfo():
    artist = freim['artist'][-1]

    file = urllib.request.urlopen('http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=' +
                                  urllib.parse.quote(artist) + '&api_key=' + urllib.parse.quote(API) +
                                  '&format=json')
    try:
        artist_info = json.loads(file.read().decode())['artist']

        if len(artist_info) != 0:
            response = "I could find this information about " + str(artist) + ":\n"
            response += "- " + artist_info["bio"]["summary"] + "\n"
            return response
    except:
        pass

    response = "Sorry, but I couldn't find any information about this artist"
    # Kui robot ei saanud leida sellist artisti, siis kustutame meie "andmebaasist" temast igasugune info
    del freim['artist'][-1]

    return response


# Otsime artisti tage
def getTagByArtist(artist):

    file = urllib.request.urlopen('http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=' +
                                  urllib.parse.quote(artist) + '&api_key=' + urllib.parse.quote(API) +
                                  '&format=json')
    try:
        tags = json.loads(file.read().decode())['artist']['tags']['tag']

        # Lisame tagid freimile tulevikuks
        for tag in tags:
            freim['tag'].append(tag['name'])

        return True
    except:
        pass

    # Kui robot ei saanud leida sellist tagi selle artisti järgi, siis kustutame meie "andmebaasist" temast igasugune info
    freim['artist'].remove(artist)

    return False


# Otsime populaarsemaid lugusid
def getTopSongs():

    file = urllib.request.urlopen('http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key=' +
                                  urllib.parse.quote(API) + '&format=json')

    tracks = json.loads(file.read().decode())["tracks"]["track"]

    # Segame kõik lood
    random.shuffle(tracks)

    response = "I'd recommend these 5 songs:\n"
    for i in range(5):
        track = tracks[i]
        response += "- \"" + track["name"] + "\" by " + track["artist"]["name"] + "\n"

        # Lisame laulu ja artisti nime tulevikuks freimile
        freim['song'].append(track['name'])
        freim['artist'].append(track['artist']['name'])

    return response



# API key
API = 'YOUR_KEY'  # Your LastFM API key
