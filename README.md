# Music helper chatbot using NLP

This project is built using MITIE: MIT Information Extraction (https://github.com/mit-nlp/MITIE) and Last FM API (https://www.last.fm/api).

Music helper chatbot is a simple python chatbot, which provides brief information about artists, albums, songs and tags. 
Using MITIE bot analyzes user's input and then sends a request using Last FM API. Then bot analyzes received document in JSON format and provides user requested information.


# Using Music Helper

Next instruction was partly taken from the official MITIE repository (https://github.com/mit-nlp/MITIE).

### Initial Setup

Before you can run the provided examples you will need to compile MITIE as a shared library.

On a UNIX like system, this can be accomplished by running `make` in the top level MITIE folder or
by running:
```
cd mitielib
make
```
This produces shared and static library files in the mitielib folder.  Or you can use
CMake to compile a shared library by typing:
```
cd mitielib
mkdir build
cd build
cmake ..
cmake --build . --config Release --target install
```

Either of these methods will create a MITIE shared library in the mitielib folder. 
Once you have built the MITIE shared library, you can go to the [examples/python](examples/python) folder and run .py scripts there.

### LastFM API key adding

In order to use this chatbot you'll need LastFM API key. Get it here: https://www.last.fm/api. 
Once you have it, navigate to examples/python/chat_ai.py, find a variable named "API" and write down your API key.

### Chatbot running
When you've done all the steps above simply run chatterbot.py or chatterbot_gui.py from the [examples/python](examples/python) folder.
