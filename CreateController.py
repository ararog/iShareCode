#
#  CreateController.py
#  IShareCode
#
#  Created by ROGERIO ARAUJO on 05/09/09.
#  Copyright (c) 2009 __MyCompanyName__. All rights reserved.
#

from objc import YES, NO, IBAction, IBOutlet
from Foundation import *
from AppKit import *
from mercurial import ui, hg, bundlerepo
from mercurial import cmdutil

class CreateController(NSWindowController):

	destinationField = objc.IBOutlet()
	closeButton = objc.IBOutlet()
	directory = None

	def __new__(cls, directory):
		return cls.alloc().initWithDirectory_(directory)

	def initWithDirectory(self, directory):
		self.directory = directory
		self = self.initWithWindowNibName_owner_("CreateWindow", self)
		self.showWindow_(self)
		self.retain()
		return self
				
	def windowWillClose(self, notification):
		self.autorelease()

	def awakeFromNib(self):
		self.destinationField.setStringValue_(self.directory)

	def create(self):
		if(self.destinationField.stringValue() is not None):
			try:
				hg.repository(cmdutil.remoteui(ui.ui(), {}), self.destinationField.stringValue(), create=1)
				NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
					NSLocalizedString("ERROR", None), "Ok", None, None, NSLocalizedString("Repository created sucessfully!", None)).runModal()
			except:
				NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
					NSLocalizedString("ERROR", None), "Ok", None, None, NSLocalizedString("An error occurred while creating Mercurial repository!", None)).runModal()
				import traceback
				traceback.print_exc()
				return ERROR(u'Exception, see traceback')
				
	
	def close(self):
		self.close()
		self.autorelease()
		
	def browse(self):
		oDirPanel = NSOpenPanel.openPanel()
		oDirPanel.setCanChooseFiles_(NO)
		oDirPanel.setCanChooseDirectories_(YES)
		if(self.destinationField.stringValue() is None):
			self.destinationField.setStringValue_(self.directory)
			
		if(oDirPanel.runModalForDirectory_file_(self.destinationField.stringValue(), None) == NSOKButton):
			self.destinationField.setStringValue_(oDirPanel.filenames()[0])