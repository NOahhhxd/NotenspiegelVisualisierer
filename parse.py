import datetime
import sys
import platform

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os

import guiscript

HELP_TEXT = """Um Elemente auszuwählen gibt es folgende Möglichkeiten:
1. Nummer (steht vor dem Modul) eingeben: 1
2. Nummern mehrerer Module eingeben: [1,3,7]
oder für mehrere hintereinanderstehende Module: [1-3]
3. Anfang des Namens eingeben: Mathe
(Damit werden alle Module ausgewählt, die so beginnen)

Um Elemente wieder zu entfernen:
1. wie beim Hinzufügen mit einem "-" davor: -1 oder -[1-3] oder -Mathe"""

aliases = {
    "Technische Informatik": "TI",
    "Grundlagen der Theoretischen Informatik": "TheoInf",
    "IT-Projektmanagement": "ITPM",
    "Logik für Informatiker": "Logik",
    "Einführung in die Informatik": "EinfInf",
    "Intelligente Systeme - Einführung": "Intelligente Systeme",
    "Programmierparadigmen": "PGP",
    "Parallele Programmierung": "PP",
    "Introduction to Robotics": "ItR",
    "Introduction to Simulation": "ItS",
    "Schlüsselkompetenzen": "Schlüko",
    "Algorithmen und Datenstrukturen": "AUD",
    "Mathematik": "Mathe",
    "Grundlagen der C++ Programmierung": "C++",
    "Computer Aided Geometric Design": "CAGD",
    "Einführung in digitale Spiele": "EIDS",
    "Allgemeine Elektrotechnik 1": "AET1",
    "Grundzüge der Algorithmischen Geometrie": "AlgoGeo"
}

### TODO: Varianten für weitere Studiengänge einfügen

halbeCPModule = [
    "Einführung in die Informatik",
    "Datenbanken I",
    "Algorithmen und Datenstrukturen",
    "Modellierung",
    "Technische Informatik I",
    "Technische Informatik II",
    "Mathematik I",
    "Mathematik II",
    "Logik für Informatiker",
    "Schlüsselkompetenzen I und II"
]


def plotModule(modules, name=None, type_="-1"):
    modules_sorted = sorted(modules, key=lambda x: float(x[1].replace(",", ".") if x[1][0].isdigit() else 1000))

    belegung: dict[str, int] = {}

    for i in modules_sorted:
        if i[1] not in belegung:
            belegung[i[1]] = 1
        else:
            belegung[i[1]] += 1

    # print(getModuleNamesFor(modules, lambda x: x[1] == "1,0"))
    labels = [str(i) + ":\n" + "\n".join(getModuleNamesFor(modules_sorted, lambda x: x[1] == i)) for i in
              belegung.keys()]

    vals = [int(i) for i in belegung.values()]
    if type_ != "-1":
        print("""Welchen Diagrammtyp willst du haben? 
Kuchendiagramm(default) => 0
Balkendiagramm          => 1""")
        type_ = input()
    if type_ == "1":
        plt.figure(figsize=(8, 18))
        plt.bar(labels, vals)
    else:
        plt.figure(figsize=(8, 6))
        plt.pie(vals, labels=labels, autopct='%1.1f%%')
    plt.title(f'Durchschnitt: {durchschnitt(modules)}')
    if name:
        plt.suptitle(f'Notenverteilung von {name}')

    fig_copy = plt.gcf()

    plt.show()
    print("Möchtest du das Bild speichern? [y|n]")
    if input().startswith("y"):
        title = input("Welchen Namen soll das Bild haben? (default: dein Name)\n")
        if title:
            fig_copy.savefig(f"{title}.png")
        else:
            fig_copy.savefig(f"{name if name else datetime.datetime.now().second}.png")
        print("gespeichert:)")


def chooseFromModules(modules, withCommandLine=True, nums=None, rec=False):
    if withCommandLine:
        if not rec:
            inf = input("Studierst du Informatik/Ingenieurinformatik? (y/n)")
            if inf.strip().lower() != "y":
                print("Wähle bitte diejenigen Module aus, die nur die halbe CP Anzahl geben.")
                global halbeCPModule
                halbeCPModule = getModuleNamesFor(chooseFromModules(modules, rec=True))
                print(halbeCPModule)
                print("okay - nun kannst du die Module auswählen, die geplottet werden sollen")
        if not nums:
            nums = set()
        else:
            nums = set(nums)

        printModules(modules)
        inp = input()
        not_found = False
        noReset = False
        while inp.lower().strip() not in ["q", ""]:
            if inp.lower().strip() in ["/help", "/?"]:
                noReset = True
                print(HELP_TEXT)
            elif inp.startswith("-"):
                inp = inp[1:]
                if inp.startswith("[") and inp.endswith("]"):
                    if inp.find("-") != -1:
                        nums_ = inp[1:-1].split("-")
                        lower = int(nums_[0])
                        upper = int(nums_[1]) + 1
                        for i in range(0 if lower < 0 else lower,
                                       len(modules) if upper >= len(modules) else upper):
                            if i in nums:
                                nums.remove(i)
                    else:
                        nums_ = inp[1:-1].split(",")
                        for j in list(filter(lambda y: y in nums,
                                             map(lambda x: int(x.strip()) if len(x.strip()) > 0 else -1, nums_))):
                            nums.remove(j)
                elif inp.startswith("*"):
                    nums.clear()
                else:
                    try:
                        num = int(inp)
                        nums.remove(num)
                    except:
                        elemsFound = [i for i, elem in enumerate(modules) if elem[0].startswith(inp)]
                        for i in elemsFound:
                            if i in nums:
                                nums.remove(i)
                        if len(elemsFound) == 0:
                            not_found = True
            elif inp.startswith("[") and inp.endswith("]"):
                if inp.find("-") != -1:
                    nums_ = inp[1:-1].split("-")
                    lower = int(nums_[0])
                    upper = int(nums_[1]) + 1
                    for i in range(0 if lower < 0 else lower,
                                   len(modules) if upper >= len(modules) else upper):
                        nums.add(i)
                else:
                    nums_ = inp[1:-1].split(",")
                    for j in list(filter(lambda y: 0 <= y < len(modules) and y not in nums,
                                         map(lambda x: int(x.strip()) if len(x.strip()) > 0 else -1, nums_))):
                        nums.add(j)
            elif inp.startswith("*"):
                nums = set(range(0, len(modules)))
            else:
                try:
                    num = int(inp)
                    if 0 <= num < len(modules) and num not in nums:
                        nums.add(num)
                except:
                    elemsFound = [i for i, elem in enumerate(modules) if elem[0].startswith(inp)]
                    for i in elemsFound:
                        nums.add(i)
                    if len(elemsFound) == 0:
                        not_found = True
            if not noReset:
                os.system("cls")
                printModules(modules, nums)
            else:
                noReset = False
            if not_found:
                print(f"Befehl {inp} ist unbekannt. Nutze /help für Erklärungen")
                not_found = False
            inp = input()
    # print(nums)
    # result = [modules[i] for i in nums]
    result = []
    if len(nums) == 0:
        nums = set(range(0, len(modules)))
    for i in nums:
        result.append(modules[i])

    return result


def filterAttributes(modulesRaw, attributNums):
    modules = []
    for module in modulesRaw:
        attributes = []
        for num in attributNums:
            if num < len(module):
                attributes.append(module[num].text.strip())
        modules.append(attributes)

    return modules


def durchschnitt(noten):
    noten = list(filter(lambda x: x[1] != "Schein", noten))
    return sum(
        [float(i[1].replace(",", ".")) * int(i[3]) * (0.5 if i[0] in halbeCPModule else 1) for i in noten]) / sum(
        [int(i[3]) * (0.5 if i[0] in halbeCPModule else 1) for i in noten])


def printModules(modules, nums=None):
    if nums:
        """
        print("\n".join(
            [f"{'[' if num in nums else ''} {num}. {i} {']' if num in nums else ''}" for num, i in
             enumerate(["\t".join(i) for i in modules])]))
        """
        for num, elem in enumerate([module[0] for module in modules]):  #: enumerate(["\t".join(i) for i in modules]):
            if num in nums:
                print(f"[{num}. {elem}]")
            else:
                print(f"{num}. {elem}")
    else:
        print("\n".join([str(num) + ". " + i for num, i in enumerate(
            [module[0] for module in modules])]))  # enumerate(["\t".join(i) for i in modules])]))


def getModuleNamesFor(modules, func=lambda x: True):
    names = []
    for module in modules:
        if func(module):
            name = module[0].replace(" (unbenotete Leistung)", "")
            for alias in aliases.keys():
                name = name.replace(alias, aliases[alias])
            names.append(name)
    return names


def modulesWithout(modules, excludesModuls):
    resModuls = []
    for module in modules:
        if module not in excludesModuls:
            resModuls.append(module)

    return resModuls


def noten_(moduls):
    noten = []
    for module in moduls:
        if not module[1].startswith("S"):
            noten.append(module[1])
    return noten


def checkPossibleFilenames():
    possibleFilenames = ["Otto-von-Guericke-Universität Magdeburg.html", "Otto-von-Guericke-Universität Magdeburg.htm"]

    for filename in possibleFilenames:
        path = os.path.join(os.getcwd(), filename)
        if os.path.exists(path):
            return filename
    return None


if __name__ == '__main__':
    filename = checkPossibleFilenames()
    if not filename:
        print(
            "Bitte geh im LSF zu deinem Notenspiegel und drücke STRG+S und speichere es in dem Ordner mit dieser Datei:) (Nicht umbenennen)")

    ### Einlesen der Datei
    soup = BeautifulSoup("\n".join(open(filename, encoding='utf-8-sig').readlines()), "html.parser")

    ### Parsen der grundlegenden Daten
    stammdaten = soup.find_all("table")[0]
    name = stammdaten.find("td").text.strip()
    # print(stammdaten)

    data = soup.find_all("table")[1]
    metaData = data.find("th")
    # print(metaData.text)

    rest = data.findAll("tr")
    # print(rest)
    cp_and_mean = rest[2]

    ### Rausfiltern der unrelevanten Daten
    rest = rest[3:-1]
    modules = []
    if platform.system() != "Darwin":
        modules = list(filter(lambda x: not str(x).startswith("<tr><td"), rest))
    else:
        modules = list(filter(lambda x: not str(x).startswith("""<tr>

﻿



	<td"""), rest))
    modules = list(map(lambda x: x.find_all("td"), modules))
    #           Modulname           Note              (nicht) bestanden     CP
    modules = [[i[1].text.strip(), i[3].text.strip(), i[4].text.strip(), i[5].text.strip()] for i in modules]

    for i, module in enumerate(modules):
        modules[i][0] = module[0].replace("Ã¼", "ü")
    for i in range(len(modules)):
        if modules[i][1] == "":
            modules[i][1] = "Schein"

    ### Beispiele
    ### Filtern nach Note, Schein, nicht bestanden
    noten = list(filter(lambda x: x[1] != "Schein", modules))
    nicht_bestanden = list(filter(lambda x: x[2] != "bestanden", modules))
    schein = list(filter(lambda x: x[1] == "Schein", modules))

    ### weitere Beispiele, um Modulgruppen zu erstellen
    """
    matheModule = list(
        filter(lambda x: x[0].startswith("Mathematik") or x[0].startswith("Grundlagen der Theo"), modules))

    # print(matheModule)
    # print(durchschnitt(matheModule))

    programming = list(filter(
        lambda x: x[0].startswith("Einführung in die Inf") or x[0].startswith("Algo") or x[0].startswith("Program"),
        modules))
    print(durchschnitt(programming))

    otherModuls = modulesWithout(modulesWithout(modules, matheModule), programming)
    print(otherModuls)
    print(noten_(otherModuls))
    print(durchschnitt(otherModuls))
    """

    ### Beispiel zum Plotten ausgewählter Module
    # plotModule(chooseFromModules(modules))
    plotModule(guiscript.visualize(modules))
