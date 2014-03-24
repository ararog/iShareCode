#
#  CommitController.py
#  IShareCode
#
#  Created by ROGERIO ARAUJO on 04/09/09.
#  Copyright (c) 2009 __MyCompanyName__. All rights reserved.
#

from objc import YES, NO, IBAction, IBOutlet
from Foundation import *
from AppKit import *
from mercurial import ui, hg
from Resource import *
from IgnoreController import *

class CommitController(NSWindowController):
	
	toolBar = objc.IBOutlet()
	tableView = objc.IBOutlet()
	textView = objc.IBOutlet()
	directory = None
	respository = None
	rowcount = 0
	files = []
	
	def __new__(cls, directory):
		return cls.alloc().initWithDirectory_(directory)

	def updateStatus(self):
		self.files = []
		states = 'modified added removed deleted unknown ignored clean'.split()
		self.repository = hg.repository(ui.ui(), self.directory)
		status = self.repository.status('.', None, None, True, True, True)	
		self.changestates = zip(states, status)
		for _state, _files in self.changestates:
			for _file in _files:
				resource = Resource()
				resource.setPath(_file)
				resource.setState(NSLocalizedString(_state, None))
				resource.setSelected(False)
				self.files.append(resource)
 
	def initWithDirectory(self, directory):
		self.directory = directory
		self = self.initWithWindowNibName_owner_("CommitWindow", self)
		self.showWindow_(self)
		self.retain()
		return self
		
	def windowWillClose(self, notification):
		self.autorelease()
		
	def awakeFromNib(self):
		self.updateStatus()
		self.rowcount = len(self.files)
		# tableView is an outlet set in Interface Builder
		self.tableView.setTarget_(self)
		self.tableView.window().setDelegate_(self)
		
	# data source methods
	def numberOfRowsInTableView(self, aTableView):
		return self.rowcount

	def tableView_objectValueForTableColumn_row(
			self, aTableView, aTableColumn, rowIndex):
		col = aTableColumn.identifier()
		if col == "selected":
			aTableColumn.dataCell().setTitle_(self.files[rowIndex].state)
			return self.files[rowIndex].selected
		else:
			return self.files[rowIndex].path

	def tableView_setObjectValue_forTableColumn_row(
		self, aTableView, anObject, aTableColumn, rowIndex):
		self.files[rowIndex].setSelected(anObject)
		self.tableView.reloadData()
	
	#Toolbar actions
	def add(self):
		filesAdded = []
		for resource in self.files:
			if resource.selected:
				filesAdded.append(resource.path)
		if(len(filesAdded) > 0):
			self.repository.add(filesAdded)
			self.refresh_()
			
	def remove(self):
		after = None
		remove, forget = deleted + clean, []
		self.repository.forget(forget)
		self.repository.remove(remove, unlink=not after)
		self.refresh_()

	def refresh(self):
		self.updateStatus()
		self.tableView.reloadData()

	def commit(self):
		message = self.textView.stringValue()
		if message is not None and len(message) > 0:
			self.repository.commit(message)
			self.refresh_()
		else:
			dialog = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
				"WARNING", "Yes", "Cancel", None, "Commit changes without a message?")
			dialog.beginSheetModalForWindow_modalDelegate_didEndSelector_contextInfo_(self.window(), self, "commitConfirm:", None)	

	def commitConfirm(self, aReturnCode, aContextInfo):
		if aReturnCode == 1000:
			self.repository.commit("")	
			self.refresh_()
		else:
			print "Nothing"
	
	def revert(self):
		pass

	def move(self):
		pass

	def undo(self):
		pass

	#Context menu actions
	def addResource(self):
		row = self.tableView.clickedRow()
		if row > 0:
			self.files[row].setSelected(True)
		self.add_()	

	def removeResource(self):
		print "Remove Resource"

	def ignoreResource(self):
		IgnoreController(self.directory, self)
