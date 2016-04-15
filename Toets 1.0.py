# -*- coding: utf-8 -*-
"""
Created on 11-4-2016

@author: Sanne Geraets

11-4-2016:
    Opzet gemaakt, zonder classes. Bestand openen, splitten op >. En begonnen
    met regular expression genereren op basis van de frequency van de 
    verschillende soorten hits.
12-4-2016:
    Verder gegaan met de eigen regular expression genereren. Vervolgens de
    accessiecode en eiwit gesplit in het volledige bestand (lijst x), vervolgens
    in het heel bestand gezocht naar het eiwit (de gegenereerde regular 
    expression), daarvan de accessiecode en soort opgeslagen in een dictionary.
"""
import re
from collections import Counter


def main():
    try:
        file = openbestand()
    except IOError:
        print("Sorry, something went wrong with opening the file")
    except FileNotFoundError:
        print("Sorry, something went wrong. There is no such file")
    lijst, x = splitten(file)
    hits = regular(lijst)
    new_regular = make_re(hits)
    zoek_again(new_regular, x)


def openbestand():
    bestand = open("ploop.fa")
    file = bestand.read()
    return file


def splitten(file):
    lijst = []
    x = file.split(">")
    for regel in x:
        if "Homo sapiens" in regel:
            lijst.append(regel)
    return lijst, x


def regular(lijst):
    zoek = []
    strings = []
    hits = []
    for x in lijst:
        zoek.append(re.findall("[AG].{4}GK[ST]", x))
    for x in zoek:
        for item in x:
            strings.append(item)
    for item in strings:
        item = item[0] + "...." + item[5:]
        hits.append(item)
    return hits


def make_re(hits):
    x = Counter(hits)
    print(x)
    hit_dict = dict(x)
    most_frequent = max(hit_dict, key=lambda key: hit_dict[key])
    new_regular = most_frequent
    return new_regular


def zoek_again(new_regular, x):
    kind_dict = {}
    acces = []
    delimiters = "|", "[", "]", ":"
    for item in x:
        blub = '|'.join(map(re.escape, delimiters))
        good = re.split(blub, item)
        acces.append(good)
#    print(acces)
    for item in acces:
        hit = re.search(new_regular, "".join(item))
        if hit is not None:
            accessiecode = item[1]
            soort = item[3]
            kind_dict[accessiecode] = soort

#    print(kind_dict)


main()
