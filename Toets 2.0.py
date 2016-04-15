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
    Alles in classes gezet
13-4-2016:
    Classes verbeterd. Commentaar in het script toegevoegd.
"""

# re wordt gebruikt in de definities: regular() en zoek_again()
# Counter wordt in de definitie make_re() gebruikt voor het tellen  hoevaak een
# patroon voorkomt bij de mens
import re
from collections import Counter


def main():
    file = Bestand("ploop.fa")
    new_regular = Regular(file.openbestand())
    new_regular.splitten()
    new_regular.regular()
    new_regular.make_re()
    kind_dict = Newdict(new_regular.make_re(), new_regular.splitten())
    kind_dict.zoek_again()
    print(kind_dict.zoek_again())


# Opent het bestand en leest het door de functie read() waardoor het nog niet 
# in een lijst staat
# Exceptionhandeling voor als het bestand niet bestaat of als er iets mis is
# met het bestand
class Bestand:
    def __init__(self, file):
        self.ploop = file

    def openbestand(self):
    # Opent en leest het bestand
        try:
            bestand = open(self.ploop)
            self.read = bestand.read()
            return self.read
        except IOError:
            print("Sorry, something went wrong with opening the file")
        except FileNotFoundError:
                print("Sorry, something went wrong. There is no such file")


# Splitst de verschillende kopjes. Elke sequentie met titel is 1 onderdeel van
# de lijst
# Daarna worden alle Homo sapiens in één lijst gezet
# In de definitie regular() wordt het juiste eiwit in de lijst, met alleen alle
# mensen erin, gezocht (door gebruik te maken van de import re)
# De hits die uit deze regular expression komen, worden in een lijst gezet. De
# plaatsen waar random letters mochten staan zijn vervangen door puntjes, zodat
# als met de geimporteerde functie Counter geteld wordt hoeveel verschillende
# hits gevonden zijn, de random stukjes niet meegerekend worden (wat in de 
# volgende definitie make_re() gedaan is)
# Hieruit is een nieuwe regular expression gekozen. Ik heb gekozen voor de
# meest voorkomende hit uit de Homo sapiens-lijst omdat dit biologisch correct
# is.
class Regular:
    def __init__(self, read):
        self.read = read

    def splitten(self):
    # Het bestand wordt gesplitst op ">" en de homo sapiens worden in een
    # lijst gezet
        self.human = []
        self.all = self.read.split(">")
        for regel in self.all:
            if "Homo sapiens" in regel:
                self.human.append(regel)
        return self.all

    def regular(self):
    # Zoekt in de lijst met homo sapiens naar het regular expression - eiwit
    # en daarna is een nieuwe regular expression opgezet door het meest
    # voorkomende eiwit van de mens te pakken.
        zoek = []
        strings = []
        self.hits = []
        for x in self.human:
            zoek.append(re.findall("[AG].{4}GK[ST]", x))
        # Uit de loop hierboven is een geneste lijst gekomen. Om deze geneste
        # lijst om te zetten naar een gewone lijst is elke gevonden hit
        # toegevoegd aan een nieuwe lijst.
        for x in zoek:
            for item in x:
                strings.append(item)
        # Bij elk eiwit die gevonden is de characters eruit
        # gehaald die niet belangrijk waren voor de regular expression voor het
        # eiwit te zoeken.
        for item in strings:
            item = item[0] + "...." + item[5:]
            self.hits.append(item)

    def make_re(self):
    # Hier is door middel van Counter getelt hoevaak een hit voorkomt en 
    # vervolgens de hit die het vaakst voorkomt gebruikt als nieuwe re
        hit_dict = dict(Counter(self.hits))
        self.new_regular = max(hit_dict, key=lambda key: hit_dict[key])
        return self.new_regular


# Vervolgens is er met de nieuwe regular expression (gekozen door de meest
# voorkomende hit te pakken die gevonden was bij de Homo sapiens) gezocht in
# het gehele bestand (een lijst waar alle organismes met hun sequenties in de
# lijst staan)
# Alle organismes en de bijbehorende accessiecode zijn in een dictionary gezet
class Newdict:
    def __init__(self, new_regular, alles):
        self.new_regular = new_regular
        self.all = alles

    def zoek_again(self):
    # In deze definitie wordt opnieuw door het hele bestand gezocht en
    # elke accessiecode en soortnaam opgeslagen in een dictionary die
    # hetzelfde eiwit heeft als de nieuwe regular expression
        self.kind_dict = {}
        acces = []
        delimiters = "|", "[", "]", ":"
        # De lijst met alle soorten erin worden gesplitst op de bovenstaande
        # delimiters om de accessiecode en species te isoleren
        for item in self.all:
            bla = "|".join(map(re.escape, delimiters))
            split = re.split(bla, item)
            acces.append(split)
        for item in acces:
            hit = re.search(self.new_regular, "".join(item))
            if hit is not None:
                accessiecode = item[1]
                soort = item[3]
                self.kind_dict[accessiecode] = soort
        return self.kind_dict

main()
