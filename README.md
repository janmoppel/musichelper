# Music helper chatbot using NLP
=====

This project is built using MITIE: MIT Information Extraction (https://github.com/mit-nlp/MITIE) and Last FM API (https://www.last.fm/api).

Music helper chatbot is a simple python chatbot, which provides brief information about artists, albums, songs and tags. 
Using MITIE bot analyzes user's input and then sends a request using Last FM API. Then bot analyzes received document in JSON format and provides user requested information.


# Using Music Helper

Next instruction was originally taken from the official MITIE repository (https://github.com/mit-nlp/MITIE).

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

### Using MITIE from a Python program

Once you have built the MITIE shared library, you can go to the [examples/python](examples/python) folder
and simply run any of the Python scripts.

If you are using a UNIX system, you can also install ``mitie`` package direcly from github:
``pip install git+https://github.com/mit-nlp/MITIE.git``.

If you are using Windows then compile MITIE using the CMake instructions shown above.
