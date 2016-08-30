#!/usr/bin/python

'''
RefMan - an interactive commandline tool for managing and querying simple BibTeX databases

Copyright (c) James Surgenor 2016
'''

import pybibtex as BibTeX
import sys

def addMode(document):
    leave = False
    while not leave:
        entryType = ""
        while entryType == "":
            entryType = raw_input("\nADD MODE\nEntry type ('q' to quit):\n> ")
        if entryType == 'q':
            leave = True
        else:
            document.addNewEntry(entryType)

def findMode(document):
    leave = False
    while not leave:
        findType = ""
        while findType == "":
            findType = raw_input("\nFIND MODE\nFind type ('q' to quit):\n> ")
        if findType == 'q':
            leave = True
        elif findType == 'h':
            print("Find Mode - available Find types:")
            print("a: author, returns all entries with a given author")
            print("t: title, returns all entries whose title contains given string")
        elif findType == 'a':
            author = raw_input("Author:\n> ")
            finds = [x for x in document.entries if author in x.getField("author")]
            for find in finds:
                print("\n" + find.toBibTeXString())
        else:
            print("Unknown - exiting safely")
            leave = True


def main():
    doc = BibTeX.BibTeX()

    saveLoc = ""

    print("\nRefMan - an interactive commandline BibTeX management tool")

    if len(sys.argv) == 2:
        doc.parse(sys.argv[1])
        saveLoc = sys.argv[1]
        print("\nLoaded: " + sys.argv[1])


    leave = False
    while not leave:
        mode = ""
        while mode == "":
            mode = raw_input("\nMODE SELECT\nMode ('q' to quit):\n> ")
        if mode == 'q':
            leave = True
        elif mode == 'add':
            addMode(doc)
        elif mode == 'find':
            findMode(doc)
        else:
            print("Unknown - exiting safely")
            leave = True

    save = raw_input("Save changes? (y/N):\n> ")
    if save == 'y':
        while saveLoc == "":
            saveLoc = raw_input("No save location known\nSave as:\n> ")
        doc.write(saveLoc)

if __name__ == '__main__':
    main()
