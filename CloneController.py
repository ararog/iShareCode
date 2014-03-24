#
#  CloneController.py
#  IShareCode
#
#  Created by ROGERIO ARAUJO on 05/09/09.
#  Copyright (c) 2009 __MyCompanyName__. All rights reserved.
#

from objc import YES, NO, IBAction, IBOutlet
from Foundation import *
from AppKit import *
from mercurial import hg, bundlerepo
from mercurial import cmdutil

class CloneController(NSWindowController):

	sourcePathCombo = objc.IBOutlet()
	destinationPathCombo = objc.IBOutlet()
	revisionField = objc.IBOutlet()	
	cancelButton = objc.IBOutlet()

	def __new__(cls, directory):
		return cls.alloc().initWithDirectory_(directory)

	def initWithDirectory(self, directory):
		self.directory = directory
		self = self.initWithWindowNibName_owner_("CloneWindow", self)
		self.showWindow_(self)
		self.retain()
		return self

	def windowWillClose(self, notification):
		self.autorelease()

	def awakeFromNib(self):
		self.sourcePathCombo.setStringValue_(self.directory)
		self.destinationPathCombo.setStringValue_(self.directory)

	def browseSourcePath(self):
		oDirPanel = NSOpenPanel.openPanel()
		oDirPanel.setCanChooseFiles_(NO)
		oDirPanel.setCanChooseDirectories_(YES)
		if(self.sourcePathCombo.stringValue() is None):
			self.sourcePathCombo.setStringValue_(self.directory)
			
		if(oDirPanel.runModalForDirectory_file_(self.sourcePathCombo.stringValue(), None) == NSOKButton):
			self.sourcePathCombo.setStringValue_(oDirPanel.filenames()[0])
		
	def browseDestinationPath(self):
		oDirPanel = NSOpenPanel.openPanel()
		oDirPanel.setCanChooseFiles_(NO)
		oDirPanel.setCanChooseDirectories_(YES)
		if(self.destinationPathCombo.stringValue() is None):
			self.destinationPathCombo.setStringValue_(self.directory)
			
		if(oDirPanel.runModalForDirectory_file_(self.destinationPathCombo.stringValue(), None) == NSOKButton):
			self.destinationPathCombo.setStringValue_(oDirPanel.filenames()[0])

	def cancel(self):
		self.close()
		self.autorelease()		