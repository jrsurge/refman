#!/usr/bin/python

'''
This is a temporary main file to test the pybibtex lib

It will eventually contain all the logic for RefMan
'''

import pybibtex as BibTeX

def main():

    doc = BibTeX.BibTeX()

    doc.addNewEntry("booklet")

    # The entries accessor is a temporary cheat - nothing is private in Python
    for entry in doc.entries:
        print("\n" + entry.toBibTeXString())

if __name__ == '__main__':
    main()
