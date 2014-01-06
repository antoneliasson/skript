#!/usr/bin/env python3
#
# If you are my future employer, you might want to stop reading now.
#
# To anyone else: This program outputs Markdown to stdout. To create a PDF, send
# it through pandoc using something like this:
#
#     ./kursutvärdering.py '/home/anton/Hämtningar/Utvärdering av TLTH:s buggkurser HT2013 - nybörjare - Sheet1.csv' | pandoc --from=markdown -o nybörjare.pdf
#
# Written in a hurry on 6 januari 2014.

import sys
import csv

## oanvänt :3
# class MultiChoice(dict):
#     # ex: Förare/följare?
#     def __init__(self, name):
#         dict.__init__(self)
#         self.name = name

# class Option:
#     # ex: Affischer
#     def __init__(self, name):
#         self.name = name
#         self.count = 0

# class FreeText:
#     # extends list?
#     def __init__(self, name, body):
#         self.name = name
#         self.body = body

def main(filepath):
    ## INIT
    interesting = {
        4 : list(), # Vad har varit bra, vad kan förbättras med musiken?
        7 : list(), # Vad har varit bra, vad kan förbättras hos tränarna?
        11 : list(), # Vad har varit bra, vad kan förbättras hos hjälptränarna?
        15 : list(), # Vad har varit bra, vad kan förbättras med undervisningen?
        19 : list(), # Vad har varit bra, vad kan förbättras med paus och fika?
        22 : list(), # Något särskilt som du vill ha mer av?
        26 : list(), # Vad har varit det bästa med kurserna?
        27 : list(), # Vad kan förbättras med kurserna?
        32 : list() # Övriga synpunkter på danssittningen:
    }

    # LÄS
    with open(filepath, newline='') as csvfile:
        # default-dialekt är 'excel' som verkar vara kommaseparerade fält,
        # omgivna av citattecken där det behövs
        spamreader = csv.reader(csvfile)
        rows = list()
        # row: lista
        for row in spamreader:
            rows.append(row)
    headers = rows[0]

    ## SAMMANFATTA
    for i in range(1, len(rows)):
        row = rows[i]
        for fieldnum in interesting:
            field = row[fieldnum].strip()
            if len(field) > 0: # ta inte med tomma svar
                interesting[fieldnum].append(field)

    ## SKRIV INLEDNING
    filename = filepath.split('/')[-1]
    segments = filename.split('.')
    name = '.'.join(segments[0:len(segments)-1])
    print(name) # dokumentrubrik
    print(len(name)*'=', end='\n\n') # understrykning, á la Markdown

    ## SKRIV DATA
    keys = list(interesting.keys())
    keys.sort()
    for fieldnum in keys:
        header = headers[fieldnum]
        answers = interesting[fieldnum]
        print(header + '\n' + 60*'-', end='\n\n') # underrubrik
        print('\n\n'.join(answers), end='\n\n') # två nyradstecken som
                                                # styckeavdelare

if __name__ == '__main__':
    if(len(sys.argv) == 2):
        main(sys.argv[1])
    else:
        print('Usage: {} <path to CSV file>'.format(sys.argv[0]))

#    main('/home/anton/Hämtningar/Utvärdering av TLTH:s buggkurser HT2013 - nybörjare - Sheet1.csv')
#    main('/home/anton/Hämtningar/Utvärdering av TLTH:s buggkurser HT2013 - fortsättning - Sheet1.csv')
