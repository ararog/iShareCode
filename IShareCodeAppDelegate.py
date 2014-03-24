#
#  IShareCodeAppDelegate.py
#  IShareCode
#
#  Created by ROGERIO ARAUJO on 04/09/09.
#  Copyright __MyCompanyName__ 2009. All rights reserved.
#

from Foundation import *
from AppKit import *

class IShareCodeAppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")
