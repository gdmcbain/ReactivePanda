"""
File IO tools.
Writing csv from array and dictionary
Reading csv to array and dictionary

Non-Reactive
"""
#import g
import csv
#from panda3d.core import Filename
#from StaticNumerics import *
from PandaSRC.FileSearch import *

def loadCSV(file):
    """
    Reads the contents of a csv file and returns an array of each row.
    """
    #print("File name string?" + str(file))
    fileReader = csv.reader(open(file.toOsSpecific(), "r"),dialect = 'excel', delimiter = ",", quotechar='"', quoting= csv.QUOTE_MINIMAL )

    arr = []
    for row in fileReader:
        arr.append(row)
    return arr

def saveCSV(file, arr):
    """
    Writes an array to the given csv file
    """
    fileWriter = csv.writer(open(file, "w"), dialect = 'excel')
    for l in arr:
        fileWriter.writerow(l)
    return


def loadDict(file, types={}, defaults = {}):
    """
    Creates a dictionary from a given csv file
    """
    arr = loadCSV(file)
    res = {}
    for l in arr:
        if len(l) == 2:
            key = l[0]
            val = l[1]
            #print("*****************"+ str(key) + " " + str(val))
            if key in types:
                val = types[key].decode(val)
                #print(str(val))
            res[key] = val
    print(str(defaults))
    for k,v in defaults.items():
        if not (k in res):
            res[k] = v
    return res

def saveDict(file, dict, types = {}):
    """
    Writes a csv file from the given dictionary
    """
    lines = []
    for k,v in dict.items():
        if k in types:
            v = types[k].encode(v)
        else:
            print("No type for " + k)
        lines.append([k, v])
    saveCSV(file, lines)

def findTexture(fileName):
    tFile = fileSearch(fileName, "lib/textures", ["jpg", "png", "jpeg"])
    if tFile is None:
        tFile = fileSearch(pandaPath + "lib/textures/default.jpg")
    return loader.loadTexture(tFile)

def findSound(fileName):
    return fileSearch(fileName, "sounds", ["wav", "mp3"])


