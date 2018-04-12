#!/usr/bin/env python
# -*- coding: utf-8 -*-

# titel:			Lagerverwaltung mit Python
# version:			GUI_V2.5_Abgabe
# programm:			StockManagementPopup.py
# author:			Toby Barnes
# creation date: 	17.03.2018
# submission date:	12.04.2018

import sys
import StockManagementCSV
from PyQt4 import QtGui, QtCore

# titel of class: 	Add()
# This class sets up the main window attributes for the pop-up "Add".
# This pop-up should be called if you want to change (add to) the inventory of the materials
#
class Add(QtGui.QMainWindow):

    def __init__(self, refresh_ptr):
	super(Add, self).__init__()
	add_popup_destruktor = self.__del__
	self.refresh = refresh_ptr
	add_popup_content = AddWidget(add_popup_destruktor)
	self.setCentralWidget(add_popup_content)
	self.setGeometry(100,100,500,280)

    def __del__(self):
	self.refresh()
	self.close()

# class title: AddWidget
# This class generates the layout and the content of the pop-up "Add".
# To initialize this class you have to pass 1 parameter.
#
# AddWidget(destructor)
# - destructor:			pass a pointer that points at the destructor of the pop-up window
#						that embeds this class as the central widget
#
class AddWidget(QtGui.QWidget):

    def __init__(self, destructor):
	super(AddWidget, self).__init__()
	self.add_popup_content(destructor)

    def add_popup_content(self, destructor):
	add_popup_layout = QtGui.QFormLayout()
	add_popup_layout.setSpacing(10)
	
	# all edit-boxes and edit-box inscriptions are defined and set into
	# the python layout
	edit_label_title = ["Artikelnummer","Lieferant","Anzahl"]
	edit_label = [0,1,2]
	self.editbox = [0,1,2]
	
	for n in range(3):
	    edit_label[n] = QtGui.QLabel(edit_label_title[n])
	    add_popup_layout.addRow(edit_label[n])
		#The last edit box is defined as a spin-box
	    if n == 2:
		self.editbox[n] = QtGui.QSpinBox()
		self.editbox[n].setRange(0,99999)
		self.editbox[n].setValue(0)
		add_popup_layout.addRow(self.editbox[n])
		#The rest of the edit boxes are defined as a line edit
	    else:
		self.editbox[n] = QtGui.QLineEdit()
		add_popup_layout.addRow(self.editbox[n])

	# the buttons to add to the material or exit the pop-up are defined 
	# and set into a horizontal box that is added into the pop-up layout
	button_add = QtGui.QPushButton(u"Material hinzufügen")
	button_exit = QtGui.QPushButton("Exit")
	button_add.clicked.connect(lambda: self.add(destructor))
	button_exit.clicked.connect(lambda: self.__del__(destructor))

	horizontal_box = QtGui.QHBoxLayout()
	horizontal_box.addWidget(button_add)
	horizontal_box.addWidget(button_exit)
	add_popup_layout.addRow(horizontal_box)
	self.setLayout(add_popup_layout)

	# this function adds to the stock of the materials
	# the information of the material are received from the edit boxes
    def add(self, destructor):
	modus = "pos"
	info_artikelnummer = unicode(self.editbox[0].text()).encode("utf-8")
	info_lieferant = unicode(self.editbox[1].text()).encode("utf-8")
	info_bestand  = unicode(self.editbox[2].value()).encode("utf-8")
	errorbox = self.errorreport
	StockManagementCSV.changematerialcount(info_artikelnummer,info_lieferant,info_bestand,modus,errorbox)
	self.__del__(destructor)

	# when this funktion is called it generates a warning message that 
	# shows the current error that is produced by the user
    def errorreport(self, message):
	msg = QtGui.QMessageBox()
	msg.setIcon(QtGui.QMessageBox.Warning)
	msg.setWindowTitle("Error Report")
	msg.setText(message)
	msg.setStandardButtons(QtGui.QMessageBox.Ok)
	msg.exec_()

    def __del__(self, destructor):
	# all edit boxes are set to the default settings
	self.editbox[0].setText("")
	self.editbox[1].setText("")
	self.editbox[2].setValue(0)
	destructor()

# title of class: 	Take()
# This class sets up the main window attributes for the pop-up "Take".
# This pop-up should be called if you want to change (take from) the inventory of the materials
#
class Take(QtGui.QMainWindow):

    def __init__(self, refresh_ptr):
	super(Take, self).__init__()
	take_popup_destruktor = self.__del__
	self.refresh = refresh_ptr
	take_popup_content = TakeWidget(take_popup_destruktor)
	self.setCentralWidget(take_popup_content)
	self.setGeometry(100,100,500,280)

    def __del__(self):
	self.refresh()
	self.close()

# class title: AddWidget
# This class generates the layout and the content of the pop-up "Take".
# To initialize this class you have to pass 1 parameter.
#
# TakeWidget(destructor)
# - destructor:			pass a pointer that points at the destructor of the pop-up window
#						that embeds this class as its central widget
#
class TakeWidget(QtGui.QWidget):

    def __init__(self, destructor):
	super(TakeWidget, self).__init__()
	self.take_popup_content(destructor)

    def take_popup_content(self, destructor):
	take_popup_layout = QtGui.QFormLayout()
	take_popup_layout.setSpacing(10)
	
	# all edit-boxes and edit-box inscriptions are defined and set into
	# the python layout
	edit_label_title = ["Artikelnummer","Lieferant","Anzahl"]
	edit_label = [0,1,2]
	self.editbox = [0,1,2]

	for n in range(3):
	    edit_label[n] = QtGui.QLabel(edit_label_title[n])
	    take_popup_layout.addRow(edit_label[n])
	    if n == 2:
		#The last edit box is defined as a spin-box
		self.editbox[n] = QtGui.QSpinBox()
		self.editbox[n].setRange(0,99999)
		self.editbox[n].setValue(0)
		take_popup_layout.addRow(self.editbox[n])
	    else:
		#The rest of the edit boxes are defined as a line edit
		self.editbox[n] = QtGui.QLineEdit()
		take_popup_layout.addRow(self.editbox[n])

	# the buttons to add to the material or exit the pop-up are defined 
	# and set into a horizontal box that is added into the pop-up layout
	button_take = QtGui.QPushButton("Material beziehen")
	button_exit = QtGui.QPushButton("Exit")
	button_take.clicked.connect(lambda: self.take(destructor))
	button_exit.clicked.connect(lambda: self.__del__(destructor))

	horizontal_box = QtGui.QHBoxLayout()
	horizontal_box.addWidget(button_take)
	horizontal_box.addWidget(button_exit)
	take_popup_layout.addRow(horizontal_box)
	self.setLayout(take_popup_layout)

	# this function takes from the stock of the materials
	# the information of the material are received from the edit boxes
    def take(self, destructor):
	modus = "neg"
	info_artikelnummer = unicode(self.editbox[0].text()).encode("utf-8")
	info_lieferant = unicode(self.editbox[1].text()).encode("utf-8")
	info_bestand  = unicode(self.editbox[2].value()).encode("utf-8")
	errorbox = self.errorreport
	StockManagementCSV.changematerialcount(info_artikelnummer,info_lieferant,info_bestand ,modus,errorbox)
	self.__del__(destructor)

	# when this function is called it generates a warning message that 
	# shows the current error that is produced by the user
    def errorreport(self, message):
	msg = QtGui.QMessageBox()
	msg.setIcon(QtGui.QMessageBox.Warning)
	msg.setWindowTitle("Error Report")
	msg.setText(message)
	msg.setStandardButtons(QtGui.QMessageBox.Ok)
	msg.exec_()

    def __del__(self, destructor):
	self.editbox[0].setText("")
	self.editbox[1].setText("")
	self.editbox[2].setValue(0)
	destructor()

# title of class: 	Take()
# This class sets up the main window attributes for the pop-up "Open".
# This pop-up should be called if you want to initiate a new material to the stock management.
#
class Open(QtGui.QMainWindow):

    def __init__(self, refresh_ptr):
	super(Open, self).__init__()
	open_popup_destruktor = self.__del__
	self.refresh = refresh_ptr
	open_popup_content = OpenWidget(open_popup_destruktor)
	self.setCentralWidget(open_popup_content)
	self.setGeometry(100,100,500,500)

    def __del__(self):
	self.refresh()
	self.close()

# class title: OpenWidget()
# This class generates the layout and the content of the pop-up "Open".
# To initialize this class you have to pass 1 parameter.
#
# OpenWidget(destructor)
# - destructor:			pass a pointer that points at the destructor of the pop-up window
#						that embeds this class as its central widget
#
class OpenWidget(QtGui.QWidget):

    def __init__(self, destructor):
	super(OpenWidget, self).__init__()
	self.open_popup_content(destructor)

    def open_popup_content(self, destructor):
	open_popup_layout = QtGui.QFormLayout()
	open_popup_layout.setSpacing(10)

	# all edit-boxes and edit-box inscriptions are defined and set into
	# the python layout
	edit_label_title = ["Artikelnummer","Lieferant","Objektbezeichnung","Wert",u"Gehäuse","Bestand"]	
	edit_label = [0,1,2,3,4,5]
	self.editbox = [0,1,2,3,4,5]

	for n in range(6):
	    edit_label[n] = QtGui.QLabel(edit_label_title[n])
	    open_popup_layout.addRow(edit_label[n])
	    if n == 5:
		#The last edit box is defined as a spin-box
		self.editbox[n] = QtGui.QSpinBox()
		self.editbox[n].setRange(0,99999)
		self.editbox[n].setValue(0)
		open_popup_layout.addRow(self.editbox[n])
	    else:
		 #The rest of the edit boxes are defined as a line edit
		self.editbox[n] = QtGui.QLineEdit()
		open_popup_layout.addRow(self.editbox[n])

	# the buttons to add to the material or exit the pop-up are defined 
	# and set into a horizontal box that is added into the pop-up layout
	button_open = QtGui.QPushButton(u"Material eröffnen")
	button_exit = QtGui.QPushButton("Exit")
	button_open.clicked.connect(lambda: self.open(destructor))
	button_exit.clicked.connect(lambda: self.__del__(destructor))

	horizontal_box = QtGui.QHBoxLayout()
	horizontal_box.addWidget(button_open)
	horizontal_box.addWidget(button_exit)
	open_popup_layout.addRow(horizontal_box)
	self.setLayout(open_popup_layout)

	# this function takes from the stock of the materials
	# the information of the material are received from the edit boxes
    def open(self, destructor):
	info_artikelnummer = (unicode(self.editbox[0].text())).encode('utf-8')
	info_lieferant = (unicode(self.editbox[1].text())).encode('utf-8')
	info_objektbezeichnung = (unicode(self.editbox[2].text())).encode('utf-8')
	info_wert = (unicode(self.editbox[3].text())).encode('utf-8')
	info_gehaeuse = (unicode(self.editbox[4].text())).encode('utf-8')
	info_bestand = (unicode(self.editbox[5].value())).encode('utf-8')
	destruktorlist = [info_artikelnummer,info_lieferant,
						info_objektbezeichnung,info_wert,
						info_gehaeuse,info_bestand]

	StockManagementCSV.addlistcsv(destruktorlist)
	StockManagementCSV.sortcsv()
	self.__del__(destructor)

    def __del__(self, destructor):
	self.editbox[0].setText("")
	self.editbox[1].setText("")
	self.editbox[2].setText("")
	self.editbox[3].setText("")
	self.editbox[4].setText("")
	self.editbox[5].setValue(0)
	destructor()
