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
    try:
        file = Bestand("ploop.fa")
        new_regular = Regular(file.openbestand())
        new_regular.splitten()
        new_regular.regular()
        new_regular.make_re()
        kind_dict = Newdict(new_regular.make_re(), new_regular.splitten())
        kind_dict.zoek_again()
        dic = kind_dict.zoek_again()
        for key in dic:
            print(key + "\t" * 2 + dic[key] + "\n")
    except FileNotFoundError:
        print("Sorry, something went wrong. There is no such file")
    except IOError:
        print("Sorry, something went wrong with opening the file")
    except ValueError:
        print("Woops, the pattern is not found in the file")
    except IndexError:
        print("Someting went wrong with finding the right index, my apology.")
        print("Try looking at your file, are you sure this is a legit fasta file?")
    except:
        print("Wow, you messed up pretty good..consult the author to fix this")


# Opent het bestand en leest het door de functie read() waardoor het nog niet 
# in een lijst staat
# Exceptionhandeling voor als het bestand niet bestaat of als er iets mis is
# met het bestand
class Bestand:
    def __init__(self, file):
        self.ploop = file

    def openbestand(self):
        bestand = open(self.ploop)
        self.read = bestand.read()
        return self.read


# Splitst het bestand en maakt een nieuwe lijst met homo sapiens, om hier een
# regular expression in te zoeken, van al deze hits is een nieuwe regular 
# expression gekozen. Ik heb gekozen voor de meest voorkomende hit uit de 
# Homo sapiens-lijst omdat dit biologisch correct is.
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
        for x in zoek:
            for item in x:
                strings.append(item)
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
