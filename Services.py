#
#  Services.py
#  IShareCode
#
#  Created by ROGERIO ARAUJO on 04/09/09.
#  Copyright (c) 2009 __MyCompanyName__. All rights reserved.
#

import objc
from Foundation import *
from AppKit import *
from CommitController import *
from SynchronizeController import *
from CreateController import *
from CloneController import *
import os

def serviceSelector(fn):
	return objc.selector(fn, signature="v@:@@o^@")
	
def ERROR(s):
	#NSLog(u"ERROR: %s" % (s,))
	return s

class Services(NSObject):

	@serviceSelector
	def commit_userData_error_(self, pboard, data, error):
		try:
			types = pboard.types()             
			pboardString = None
			if NSStringPboardType in types:
				pboardString = pboard.stringForType_(NSStringPboardType)
			if pboardString is None:
				NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
					NSLocalizedString("ERROR", None), "Ok", None, None, "Please select a directory/file on Finder!").runModal()

			CommitController(pboardString)

			return ERROR(None)
		except:
			NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
				NSLocalizedString("ERROR", None), "Ok", None, None, NSLocalizedString("The selected directory/file doesn't belongs to a valid Mercurial repository!", None)).runModal()
			import traceback
			traceback.print_exc()
			return ERROR(u'Exception, see traceback')

	@serviceSelector
	def synchronize_userData_error_(self, pboard, data, error):
		try:
			types = pboard.types()             
			pboardString = None
			if NSStringPboardType in types:
				pboardString = pboard.stringForType_(NSStringPboardType)
			if pboardString is None:
				NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
					NSLocalizedString("ERROR", None), "Ok", None, None, "Please select a directory/file on Finder!").runModal()

			SynchronizeController(pboardString)

			return ERROR(None)
		except:
			NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
				NSLocalizedString("ERROR", None), "Ok", None, None, NSLocalizedString("The selected directory/file doesn't belongs to a valid Mercurial repository!", None)).runModal()
			import traceback
			traceback.print_exc()
			return ERROR(u'Exception, see traceback')
		
	@serviceSelector
	def create_userData_error_(self, pboard, data, error):
		try:
			types = pboard.types()             
			pboardString = None
			if NSStringPboardType in types:
				pboardString = pboard.stringForType_(NSStringPboardType)
			if pboardString is None:
				NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
					NSLocalizedString("ERROR", None), "Ok", None, None, "Please select a directory/file on Finder!").runModal()
			
			if(os.path.exists(pboardString + "/.hg")):
				NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
					NSLocalizedString("ERROR", None), "Ok", None, None, "Repository already exists!").runModal()
			else:
				CreateController(pboardString)

			return ERROR(None)
		except:
			NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
				NSLocalizedString("ERROR", None), "Ok", None, None, NSLocalizedString("An error occurred while creating Mercurial repository!", None)).runModal()
			import traceback
			traceback.print_exc()
			return ERROR(u'Exception, see traceback')
		
	@serviceSelector
	def clone_userData_error_(self, pboard, data, error):
		try:
			types = pboard.types()             
			pboardString = None
			if NSStringPboardType in types:
				pboardString = pboard.stringForType_(NSStringPboardType)
			if pboardString is None:
				NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
					NSLocalizedString("ERROR", None), "Ok", None, None, "Please select a directory/file on Finder!").runModal()

			CloneController(pboardString)

			return ERROR(None)
		except:
			NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
				NSLocalizedString("ERROR", None), "Ok", None, None, "An error occurred while cloning Mercurial repository!").runModal()
			import traceback
			traceback.print_exc()
			return ERROR(u'Exception, see traceback')
