#!/usr/bin/env python
# -*- coding: utf-8 -*-

# titel:		Lagerverwaltung mit Python
# version:		GUI_V2.5
# programm:		StockManagement.py
# author:		Toby Barnes
# creation date: 	17.03.2018
# submission date:	12.04.2018

import sys, csv
from PyQt4 import QtGui, QtCore
import StockManagementCSV, StockManagementPopup


# titel of class: 	GuiWindow
# This class sets up the main window attributs for the gui.
class GuiWindow(QtGui.QMainWindow):

    def __init__(self):
	super(GuiWindow, self).__init__()
	self.showFullScreen()
	popup_pointer = self.create_popup
	destruktor = self.__del__
	gui_content = GuiWidget(popup_pointer, destruktor)
	self.refreshptr = gui_content.refresh
	self.setCentralWidget(gui_content)

    def create_popup(self, popup):
	if (str(popup) == str("add")):
	    self.dialog = StockManagementPopup.Add(self.refreshptr)
	    self.dialog.show()
	if (str(popup) == str("take")):
	    self.dialog = StockManagementPopup.Take(self.refreshptr)
	    self.dialog.show()
	if (str(popup) == str("open")):
	    self.dialog = StockManagementPopup.Open(self.refreshptr)
	    self.dialog.show()

    def __del__(self):
	sys.exit()

# class title: GuiWidget
# This class generates the layout and the content of the gui.
# To declare the class, you have to pass 2 parameters
# GuiWidget(popup_function, destruktor)
# - popup_function: 	pass a pointer that points at a popup creating function
# - destruktor:			pass a pointer that points at the destruktor of the main window
#								that embeds this class as its centralWidget
class GuiWidget(QtGui.QWidget):

    def __init__(self, popup_ptr, destruktor_ptr):
	super(GuiWidget, self).__init__()
	self.content(popup_ptr, destruktor_ptr)

    def content(self, popup_ptr, destruktor_ptr):
	layout_grid = QtGui.QGridLayout()
	self.setLayout(layout_grid)

	# The buttons that open a popup or shuts the programm down 
	# are defined and set into the layout
	button = [0,1,2,3,4]
	button_title = [u"Material auffüllen", "Material beziehen", u"Material eröffnen", "Programm schliessen"]
	button_style_sheet = ["background-color:rgb(0,100,255,30)",		#rgb color = light blue with 30% transparency
			"background-color:rgb(255,255,0,30)",			#rgb color = yellow with 30% transparency
			"background-color:rgb(0,255,0,30)",			#rgb color = green with 30% transparency
			"background-color:rgb(255,0,0,30)"]			#rgb color = red with 30% transparency
	feature = ["add","take","open"]

	for n in range(4):
	# the fourth button is used to shut the program down
	    if n == 3:
		button[n] = QtGui.QPushButton(button_title[n])
		button[n].clicked.connect(lambda clicked, n=n: destruktor_ptr())
		button[n].setStyleSheet(button_style_sheet[n])
		layout_grid.addWidget(button[n],0,n)
	# the other buttons open a popup
	    else:
		button[n] = QtGui.QPushButton(button_title[n])
		button[n].clicked.connect(lambda clicked, n=n: popup_ptr(feature[n]))
		button[n].setStyleSheet(button_style_sheet[n])
		layout_grid.addWidget(button[n],0,n)

	# the label that describes the material attributes 
	# are defined and set into the layout
	material_attribute = [0,1,2,3,4,5]
	material_attribute_title = ["Artikelnummer","Lieferant","Objektbezeichnung","Wert",u"Gehäuse","Bestand"]
	for x in range(6):
	    material_attribute_font = QtGui.QFont()
	    material_attribute_font.setBold(True)
	    material_attribute[x] = QtGui.QLabel(material_attribute_title[x])
	    material_attribute[x].setFont(material_attribute_font)
		#rgb color = grey with 30% transparency
	    material_attribute[x].setStyleSheet("background-color:rgb(189,189,189)")	
	    material_attribute[x].setAlignment(QtCore.Qt.AlignCenter)
	    layout_grid.addWidget(material_attribute[x],1,x)

	# this is the first initialization of the current material is generated
	# and set into the layout 
	list_csv = list(StockManagementCSV.getreducedcsvlist())
	length_csv_y = len(list_csv)
	length_csv_x = len(list_csv[0])
	max_label_y = 35

	self.material = [["" for x in range(length_csv_x)] for y in range(max_label_y)]

	for y in range(max_label_y):
	    for x in range(length_csv_x):
		if (y < length_csv_y) and (x < length_csv_x):
		# the current string has to be decoded to the ascii utf-8
		    decoded_text = (list_csv[y][x]).decode("utf-8")
		    self.material[y][x] = QtGui.QLabel(decoded_text)
		    layout_grid.addWidget((self.material[y][x]), y+2, x)
		else:
		    self.material[y][x] = QtGui.QLabel("")
		    layout_grid.addWidget((self.material[y][x]), y+2, x)
		if ((y % 2) == 1):
		#rgb color = light grey with 30% transparency
		    self.material[y][x].setStyleSheet("background-color:rgb(230,230,230)")

	# the buttons that navigate throo the material list is defined 
	# and set into the layout
	up = QtGui.QPushButton(" Page UP ")
	down = QtGui.QPushButton(" Page DOWN ")
	up.setFixedWidth(130)
	down.setFixedWidth(130)
	up.clicked.connect(lambda: self.pageup())
	down.clicked.connect(lambda: self.pagedown())
	up.setStyleSheet("background-color:rgb(255,165,0,30)")
	down.setStyleSheet("background-color:rgb(255,165,0,30)")
	layout_grid.addWidget(up,0,6)
	layout_grid.addWidget(down,37,6)

	# this function when called, makes a refresh of the curren material 
	# list that is presented on the gui
    def refresh(self):
	list_csv = list(StockManagementCSV.getreducedcsvlist())
	length_csv_y = len(list_csv)
	length_csv_x = len(list_csv[0])
	max_label_y = 35

	for y in range(max_label_y):
	    for x in range(length_csv_x):
		if (y < length_csv_y) and (x < length_csv_x):
			# the current string has to be decoded to the ascii utf-8
		    decoded_text = (list_csv[y][x]).decode("utf-8")
		    self.material[y][x].setText(decoded_text)
		else:
		    self.material[y][x].setText("")

    def pageup(self):
	StockManagementCSV.changepage(int(-1))
	self.refresh()

    def pagedown(self):
	StockManagementCSV.changepage(int(+1))
	self.refresh()

def main():
    app = QtGui.QApplication(sys.argv)
    gui = GuiWindow()
    gui.show()
    sys.exit(app.exec_())

# (if) block will only run if that python file is the entry point to your program
if __name__ == "__main__":
	main()
