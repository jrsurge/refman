#!/usr/bin/python

'''
This is a temporary main file to test the pybibtex lib

It will eventually contain all the logic for RefMan
'''

import pybibtex as BibTeX

def main():

    doc = BibTeX.BibTeX()

    doc.parse("test.bib")

    doc.addNewEntry("booklet")

    doc.write("test.bib")

if __name__ == '__main__':
    main()
