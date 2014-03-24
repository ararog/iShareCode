#
#  IgnoreController.py
#  IShareCode
#
#  Created by ROGERIO ARAUJO on 05/09/09.
#  Copyright (c) 2009 __MyCompanyName__. All rights reserved.
#

from __future__ import with_statement 
from objc import YES, NO, IBAction, IBOutlet
from Foundation import *
from AppKit import *
from mercurial import ui, hg
from Resource import *
import os

class IgnoreController(NSWindowController):

	globField = objc.IBOutlet()
	regexpField = objc.IBOutlet()
	filtersTableView = objc.IBOutlet()
	filesTableView = objc.IBOutlet()
	
	buttonRefresh = objc.IBOutlet()
	buttonRemoveSelected = objc.IBOutlet()
	
	filesDataSource = None
	filtersDataSource = None
	directory = None
	repository = None
	files = []
	filters = []
	
	parentController = None

	def __new__(cls, directory, parentController):
		return cls.alloc().initWithDirectory_(directory, parentController)

	def updateFilters(self):
		self.filters = []
		arquivo = self.directory + "/.hgignore"
		if os.path.exists(arquivo):
			with open(arquivo, "r") as ignoreFile:
				for line in ignoreFile:
					self.filters.append(line)
		
	def updateStatus(self):
		self.files = []
		states = 'modified added removed deleted unknown ignored clean'.split()
		self.repository = hg.repository(ui.ui(), self.directory)
		status = self.repository.status('.', None, None, True, True, True)	
		self.changestates = zip(states, status)
		for _state, _files in self.changestates:
			if _state != "ignored":
				for _file in _files:
					self.files.append(_file)

	def saveFilters(self):		
		arquivo = self.directory + "/.hgignore"
		with open(arquivo, "w") as ignoreFile:
			for filter in self.filters:
				ignoreFile.write(filter + "\n")
		
	def initWithDirectory(self, directory, parentController):
		self.directory = directory
		self.parentController = parentController
		self = self.initWithWindowNibName_owner_("IgnoreWindow", self)
		self.showWindow_(self)
		self.retain()
		return self

	def windowWillClose(self, notification):
		self.parentController.updateStatus()
		self.autorelease()

	def awakeFromNib(self):
		self.updateStatus()
		self.filesDataSource = ItemsDatasource.alloc().initWithItems_(self.files, self.filesTableView)
		self.filesTableView.setDataSource_(self.filesDataSource)
		self.filesTableView.setDelegate_(self.filesDataSource)
		self.filesTableView.setTarget_(self)
		self.filesTableView.window().setDelegate_(self)	
		if len(self.files) == 0:
			self.buttonRefresh.setEnabled_(False)

		self.updateFilters()	
		self.filtersDataSource = ItemsDatasource.alloc().initWithItems_(self.filters, self.filtersTableView)
		self.filtersTableView.setDataSource_(self.filtersDataSource)
		self.filtersTableView.setDelegate_(self.filtersDataSource)
		self.filtersTableView.setTarget_(self)
		self.filtersTableView.window().setDelegate_(self)	
		if len(self.filters) == 0:
			self.buttonRemoveSelected.setEnabled_(False)

	#Buttons actions
	def addGlob(self):
		if(self.globField.stringValue() is not None and len(self.globField.stringValue()) > 0):
			self.filters.append("glob:" + self.globField.stringValue()) 
			self.globField.setStringValue_("")
			self.refresh_()
		
	def addRegexp(self):
		if(self.regexpField.stringValue() is not None and len(self.regexpField.stringValue()) > 0):
			self.filters.append("regexp:" + self.regexpField.stringValue()) 
			self.regexpField.setStringValue_("")
			self.refresh_()
		
	def removeSelected(self):
		self.filters.pop(self.filtersTableView.clickedRow())
		self.refresh_()
				
	def refresh(self):
		self.saveFilters()
		self.updateStatus()
		self.filesDataSource.setItems(self.files)
		if len(self.files) == 0:
			self.buttonRefresh.setEnabled_(False)
		else:	
			self.buttonRefresh.setEnabled_(True)

		self.filtersDataSource.setItems(self.filters)
		if len(self.filters) == 0:
			self.buttonRemoveSelected.setEnabled_(False)
		else:	
			self.buttonRemoveSelected.setEnabled_(True)

		
class ItemsDatasource(NSObject):

	tableView = None
	items = []

	def initWithItems(self, items, tableView):
		self = self.init()
		self.items = items
		self.tableView = tableView
		return self
		
	def setItems(self, items):
		self.items = items
		self.tableView.reloadData()
		
	# data source methods
	def numberOfRowsInTableView(self, aTableView):
		return len(self.items)

	def tableView_objectValueForTableColumn_row(
			self, aTableView, aTableColumn, rowIndex):
		return self.items[rowIndex]
