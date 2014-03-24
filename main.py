#
#  main.py
#  IShareCode
#
#  Created by ROGERIO ARAUJO on 04/09/09.
#  Copyright __MyCompanyName__ 2009. All rights reserved.
#

#import modules required by application
import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib
from Services import *

services = Services.alloc().init()
NSRegisterServicesProvider(services, u"IShareCode")
AppKit.NSUpdateDynamicServices()

# pass control to AppKit
AppHelper.runEventLoop()
