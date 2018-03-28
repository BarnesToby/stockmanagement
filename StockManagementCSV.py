#!/usr/bin/env python
# -*- coding: utf-8 -*-

# titel:		Lagerverwaltung mit Python
# version:		GUI_V2.5
# programm:		StockManagementCSV.py
# author:		Toby Barnes
# creation date: 	17.03.2018
# submission date:	12.04.2018

import sys, csv, operator

# define global variable 
page = 0

# titel of function: 	readcsv()
# This function returns a list of the current materials and its property
#
def readcsv():
    file = open('Material.csv','r')
    readlist = csv.reader(file, delimiter=";", quotechar="'")
    returnlist = list(readlist)
    file.close()
    return returnlist

# titel of function: 	getreducedcsvlist()
# This function returns a list reduced list that is dependent of the current page
#
def getreducedcsvlist():
    file = open('Material.csv','r')
    readlist = csv.reader(file, delimiter=";", quotechar="'")
    prozesslist = list(readlist)
    file.close()

    global page
    listlength = len(prozesslist)
    maxlengthinpage = 35
    maxpage = getmaxpages()
    maxlength_y = (listlength % maxlengthinpage)
    returnlist = [["" for x in range(6)] for y in range(maxlengthinpage)]

    for y in range(maxlengthinpage):
	for x in range(6):
	    current_y = (y+(page*maxlengthinpage))
	    if(page < maxpage):
		returnlist[y][x] = prozesslist[current_y][x]
	    if(page == maxpage):
		if(y < maxlength_y):
		    returnlist[y][x] = prozesslist[current_y][x]
		elif(y >= maxlength_y):
		    returnlist[y][x] = ""
		else:
		    print("Fehler: 0x01")
    return (returnlist)

# titel of function: 	getmaxpages()
# this function returns the maximum amount of pages the Gui should show
#
def getmaxpages():
    file = open('Material.csv','r')
    readlist = csv.reader(file, delimiter=";", quotechar="'")
    prozesslist = list(readlist)
    file.close()

    listlength = len(prozesslist)
    maxlengthinpage = 35
    maxpage = int(listlength/maxlengthinpage)
    return(maxpage)

# titel of function: 	changepage(number)
# this function changes the current page
# you have to pass 1 parameter
# normally you pass +1(page) or -1(page)
#
def changepage(number):
    global page
    tempvar = (int(page)+int(number))
    if(page == 0):
	if((tempvar < (getmaxpages())) and (tempvar > 0)):
	    page = tempvar
    elif(page == (getmaxpages())):
	if(tempvar < (getmaxpages())):
	    page = tempvar
    else:
	page = tempvar

# titel of function: 	addlistcsv(attendlist)
# this function attends a list into the csv file
# one parameter is required to call this function
# parameter: attendlist = [artikelnummer,lieferant,objektbezeichnung,wert,gehaeuse,bestand]
#
def addlistcsv(attendlist):
    file = open('Material.csv','a')
    rewritelist = csv.writer(file, delimiter=";", quotechar="'", quoting=csv.QUOTE_MINIMAL)
    rewritelist.writerow(attendlist)
    file.close()

# titel of function: 	writelistcsv(writelist)
# This function overwrits a list of the csv file.
# One parameter is required to call this function.
# parameter: writelist = [x][artikelnummer,lieferant,objektbezeichnung,wert,gehaeuse,bestand]
# Warning!!!: This funktion could delete all your saved materials in the csv file.
#
def writelistcsv(writelist):
    file = open('Material.csv','w')
    overwritelist = csv.writer(file, delimiter=";", quotechar="'", quoting=csv.QUOTE_MINIMAL)
    overwritelist.writerows(writelist)
    file.close

# titel of function: 	sortcsv()
# This function sorts the csv-file by the first column
#
def sortcsv():
    currentlist = list(readcsv())
    sortinglist = sorted(currentlist, key = operator.itemgetter(0))

    file = open('Material.csv','w')
    writelist = csv.writer(file, delimiter=";", quotechar="'")
    writelist.writerows(sortinglist)
    file.close()

# titel of function: 	sortcsv(sortnum)
# This function sorts the csv-file by the column that the parameter refers to.
# One parameter is required that the function can be called.
# parameter sortnum: should be an int between 0 to 5
#
def sortcsvby(sortrow):
    currentlist = list(readcsv())
    sortinglist = sorted(currentlist, key = operator.itemgetter(sortrow))

    file = open('Material.csv','w')
    writelist = csv.writer(file, delimiter=";", quotechar="'")
    writelist.writerows(sortinglist)
    file.close()

# titel of function: 	changematerialcount(artikelnummer, lieferant, anzahl, modus, errorpopup)
# This function changes the inventory of the materials based on the parameter modus you pass.
# parameters
#	- artikelnummer: pass a "artikelnummer" string that exist in your csv file
#	- lieferant: pass a "lieferant" string that exist in your csv file
#	- anzahl: pass a int number that you want to add or take from the inventory of a material
#	- modus: pass a "pos" if you want to add to the inventory or
#			 pass a "neg" if you want to take from the inventory
#	- errorpopup: pass a error popup function that can be called if one of these
#					attributes are not recognised in the csv file
#
def changematerialcount(artikelnummer, lieferant, anzahl, modus, errorpopup):
    currentlist = list(readcsv())
    listlength = len(currentlist)
    errorflag = False

    for x in range(0,listlength):
	if artikelnummer == (currentlist[x][0]):
	    errorflag = True
	    if lieferant == (currentlist[x][1]):
		if modus == "neg":
		    currentlist[x][5] = (int(currentlist[x][5]) - int(anzahl))
		elif modus == "pos":
		    currentlist[x][5] = (int(currentlist[x][5]) + int(anzahl))
		else:
		    error = "Fehler: Rechnungsmodus wurde nicht erkannt"
		    print(error)
		    errorpopup(error)
		    break
	    else:
		error = "Fehler: Lieferant wurde nicht erkannt"
		print(error)
		errorpopup(error)

    if errorflag == False:
	error = "Fehler: Artikelnummer wurde nicht erkannt"
	print(error)
	errorpopup(error)
    else:
	writelistcsv(currentlist)

