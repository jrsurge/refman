#!/usr/bin/python

'''
pybibtex.py

This file was created as part of RefMan - an interactive command line tool for
managing and querying simple BibTeX databases

Copyright (c) James Surgenor 2016
'''

class BibTeX:
    '''
    This is our main object class - primarily to encapsulate our data and
    represent a BibTeX document

    Methods with capitals are Pattern-like functions
    '''
    def __init__(self):
        self.entries = []

    def parse(self, path):
        '''
        Parse from a file

        This assumes a valid BibTeX file, and doesn't check for missing requiredFields - if you
        want to break format, you can add strange entries manually this way and void checking
        '''
        # make sure we're starting again
        self.entries = []

        rawdoc = ""
        with open(path, 'r') as f:
            rawdoc = f.read()

        # minimise doc
        rawdoc = rawdoc.replace('\n','').replace('\t','').replace('  ','').replace('    ','')

        # split on @ and ignore anything that's empty or with a %
        ents = [x for x in rawdoc.split("@") if x != '' and "%" not in x]

        # create all the entries - prepare for some Python oneliner voodoo..
        for ent in ents:
            data = ent.split("{",1)

            tmpEnt = self.Factory(data[0])
            tmpEnt.setCiteKey(data[1].split(',', 1)[0])

            flds = [ x.split('={') for x in data[1].split(',',1)[1].split('},') ]
            flds[-1][-1] = flds[-1][-1].replace('}}','')

            for k, v in flds:
                tmpEnt.setField(k, v)

            self.addEntry(tmpEnt)

    def write(self, path):
        '''
        Write existing database to file
        '''
        with open(path,'w') as f:
            for entry in self.entries:
                f.write(entry.toBibTeXString() + '\n\n')

    def Builder(self,entry):
        '''
        An interactive 'Builder' pattern function for initialising
        new Entry objects
        '''
        print("{}".format(entry.getType()))
        keyExists = True
        citeKey = ""
        while(keyExists):
            while(citeKey == ""):
                citeKey = raw_input("Cite key:\n> ")
            if citeKey not in [ent.getCiteKey() for ent in self.entries]:
                keyExists = False
            else:
                citeKey = ""
                print("Cite key already exists in database")
        entry.setCiteKey(citeKey)

        print("\nRequired fields:")
        for key, value in entry.requiredFields():
            v = ""
            while(v == ""):
                v = raw_input("{}: ".format(key))
            entry.setField(key,v)

        print("\nOptional fields:")
        for key, value in entry.optionalFields():
            v = raw_input("{}: ".format(key))
            entry.setField(key,v)


    def Factory(self,entryType):
        '''
        A 'Factory' function for producing Entry objects
        '''
        ent = 0
        if entryType == 'article':
            ent = Article()
        elif entryType == 'book':
            ent = Book()
        elif entryType == 'booklet':
            ent = Booklet()
        elif entryType == 'conference':
            ent = Conference()
        elif entryType == 'inbook':
            ent = Inbook()
        elif entryType == 'incollection':
            ent = Incollection()
        elif entryType == 'inproceedings':
            ent = Inproceedings()
        elif entryType == 'manual':
            ent = Manual()
        elif entryType == 'mastersthesis':
            ent = MastersThesis()
        elif entryType == 'misc':
            ent = Misc()
        elif entryType == 'phdthesis':
            ent = PhDThesis()
        elif entryType == 'proceedings':
            ent = Proceedings()
        elif entryType == 'techreport':
            ent = TechReport()
        elif entryType == 'unpublished':
            ent = Unpublished()

        assert(ent != 0)
        return ent


    def addNewEntry(self,entryType):
        '''
        Automatically creates, builds and adds a new Entry objects
        to our database
        '''
        tmp = self.Factory(entryType)
        self.Builder(tmp)
        self.addEntry(tmp)

    def addEntry(self, entry):
        '''
        Adds an existing Entry instance to the database

        If the cite key already exists, append a number, then add
        '''
        if entry.getCiteKey() in [ent.getCiteKey() for ent in self.entries]:
            entry.setCiteKey(entry.getCiteKey() + '1')
        self.entries.append(entry)


class Entry:
    '''
    A VERY simplified 'abstract' class representing a BibTeX entry
    '''
    def __init__(self):
        self.type = ""
        self.citekey = ""
        self.fields = []

    def _addField(self, key, value=""):
        if key not in [x[0] for x in self.fields]:
            self.fields.append([key,value])

    def _setType(self, newType):
        self.type = newType
        return self

    def setField(self, key, newValue):
        for ind, [k,v] in enumerate(self.fields):
            if k == key:
                if v != newValue:
                    self.fields[ind][1] = newValue
                break
        return self

    def getField(self, key):
        for k, v in self.fields:
            if k == key:
                return v

    def setCiteKey(self, newKey):
        if self.citekey != newKey:
            self.citekey = newKey
        return self

    def getCiteKey(self):
        return self.citekey

    def getType(self):
        return self.type

    def requiredFields(self):
        '''
        Abstract function to return required fields..
        '''
        raise NotImplementedError

    def optionalFields(self):
        '''
        Abstract function to return optional fields..
        '''
        raise NotImplementedError

    def toBibTeXString(self):
        '''
        This function returns the BibTeX formatted string
        for writing to file
        '''

        bibString = "@{}{}{},\n".format(self.type, "{", self.citekey)

        for key, value in [x for x in self.fields if x[1] != ""]:
            bibString += "    {}={}{}{},\n".format(key,"{", value, "}")

        bibString = bibString[:-2]
        bibString += "\n}"

        return bibString


class Article(Entry):
    def __init__(self):
        Entry.__init__(self)

        self._setType("article")

        self._addField("title")
        self._addField("author")
        self._addField("journal")
        self._addField("year")

        self._addField("volume")
        self._addField("number")
        self._addField("pages")
        self._addField("month")
        self._addField("note")
        self._addField("key")

    def requiredFields(self):
        return self.fields[:4]

    def optionalFields(self):
        return self.fields[4:]


class Book(Entry):
    def __init__(self):
        Entry.__init__(self)

        self._setType("book")

        self._addField("title")
        self._addField("author")
        self._addField("publisher")
        self._addField("year")

        self._addField("volume")
        self._addField("series")
        self._addField("address")
        self._addField("edition")
        self._addField("month")
        self._addField("note")
        self._addField("key")

    def requiredFields(self):
        return self.fields[:4]

    def optionalFields(self):
        return self.fields[4:]


class Booklet(Entry):
    def __init__(self):
        Entry.__init__(self)

        self._setType("booklet")

        self._addField("title")

        self._addField("author")
        self._addField("howpublished")
        self._addField("address")
        self._addField("month")
        self._addField("year")
        self._addField("note")
        self._addField("key")

    def requiredFields(self):
        return self.fields[:1]

    def optionalFields(self):
        return self.fields[1:]


class Conference(Entry):
    def __init__(self):
        Entry.__init__(self)

        self._setType("conference")

        self._addField("title")
        self._addField("author")
        self._addField("booktitle")
        self._addField("year")

        self._addField("editor")
        self._addField("pages")
        self._addField("organization")
        self._addField("publisher")
        self._addField("address")
        self._addField("month")
        self._addField("note")
        self._addField("key")

    def requiredFields(self):
        return self.fields[:4]

    def optionalFields(self):
        return self.fields[4:]

class Inbook(Entry):
    def __init__(self):
        Entry.__init__(self)

        self._setType("inbook")

        self._addField("title")
        self._addField("author")
        self._addField("chapter")
        self._addField("pages")
        self._addField("publisher")

        self._addField("volume")
        self._addField("series")
        self._addField("address")
        self._addField("edition")
        self._addField("month")
        self._addField("note")
        self._addField("key")

    def requiredFields(self):
        return self.fields[:5]

    def optionalFields(self):
        return self.fields[5:]

class Incollection(Entry):
    def __init__(self):
        Entry.__init__(self)

        self._setType("incollection")

        self._addField("title")
        self._addField("author")
        self._addField("booktitle")
        self._addField("year")

        self._addField("editor")
        self._addField("pages")
        self._addField("organization")
        self._addField("publisher")
        self._addField("address")
        self._addField("month")
        self._addField("note")
        self._addField("key")

    def requiredFields(self):
        return self.fields[:4]

    def optionalFields(self):
        return self.fields[4:]

class Inproceedings(Entry):
    def __init__(self):
        Entry.__init__(self)

        self._setType("inproceedings")

        self._addField("title")
        self._addField("author")
        self._addField("booktitle")
        self._addField("year")

        self._addField("editor")
        self._addField("pages")
        self._addField("organization")
        self._addField("publisher")
        self._addField("address")
        self._addField("month")
        self._addField("note")
        self._addField("key")

    def requiredFields(self):
        return self.fields[:4]

    def optionalFields(self):
        return self.fields[4:]

class Manual(Entry):
    def __init__(self):
        Entry.__init__(self)

        self._setType("manual")

        self._addField("title")

        self._addField("author")
        self._addField("organization")
        self._addField("address")
        self._addField("edition")
        self._addField("month")
        self._addField("year")
        self._addField("note")
        self._addField("key")

    def requiredFields(self):
        return self.fields[:1]

    def optionalFields(self):
        return self.fields[1:]

class MastersThesis(Entry):
    def __init__(self):
        Entry.__init__(self)

        self._setType("mastersthesis")

        self._addField("title")
        self._addField("author")
        self._addField("school")
        self._addField("year")

        self._addField("address")
        self._addField("month")
        self._addField("note")
        self._addField("key")

    def requiredFields(self):
        return self.fields[:4]

    def optionalFields(self):
        return self.fields[4:]

class Misc(Entry):
    def __init__(self):
        Entry.__init__(self)

        self._setType("misc")

        self._addField("title")
        self._addField("author")
        self._addField("howpublished")
        self._addField("month")
        self._addField("year")
        self._addField("note")
        self._addField("key")

    def requiredFields(self):
        return []

    def optionalFields(self):
        return self.fields

class PhDThesis(Entry):
    def __init__(self):
        Entry.__init__(self)

        self._setType("phdthesis")

        self._addField("title")
        self._addField("author")
        self._addField("school")
        self._addField("year")

        self._addField("address")
        self._addField("month")
        self._addField("note")
        self._addField("key")

    def requiredFields(self):
        return self.fields[:4]

    def optionalFields(self):
        return self.fields[4:]

class Proceedings(Entry):
    def __init__(self):
        Entry.__init__(self)

        self._setType("proceedings")

        self._addField("title")
        self._addField("year")

        self._addField("editor")
        self._addField("publisher")
        self._addField("organization")
        self._addField("address")
        self._addField("month")
        self._addField("note")
        self._addField("key")

    def requiredFields(self):
        return self.fields[:2]

    def optionalFields(self):
        return self.fields[2:]


class TechReport(Entry):
    def __init__(self):
        Entry.__init__(self)

        self._setType("techreport")

        self._addField("title")
        self._addField("author")
        self._addField("institution")
        self._addField("year")

        self._addField("type")
        self._addField("number")
        self._addField("address")
        self._addField("month")
        self._addField("note")
        self._addField("key")

    def requiredFields(self):
        return self.fields[:4]

    def optionalFields(self):
        return self.fields[4:]

class Unpublished(Entry):
    def __init__(self):
        Entry.__init__(self)

        self._setType("unpublished")

        self._addField("title")
        self._addField("author")
        self._addField("note")

        self._addField("month")
        self._addField("year")
        self._addField("key")

    def requiredFields(self):
        return self.fields[:3]

    def optionalFields(self):
        return self.fields[3:]
