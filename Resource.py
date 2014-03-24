#
#  Resource.py
#  IShareCode
#
#  Created by ROGERIO ARAUJO on 04/09/09.
#  Copyright (c) 2009 __MyCompanyName__. All rights reserved.
#
from Foundation import *

class Resource:

	path = None
	state = None
	selected = False

	def setPath(self, value):
		self.path = value
		
	def path(self):
		return self.path

	def setState(self, value):
		self.state = value
		
	def state(self):
		return self.state
	
	def setSelected(self, value):
		self.selected = value
		
	def selected(self):
		return self.selected
		