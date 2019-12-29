#
# Module: settings
# This file contains the code for saving and loading the settings from the EV3 brick.
#
# The settings currently include the following
#   textSize - integer
#       The height of the text in degrees. 8 degrees roughly translates to 1 millimeter vertically, so
#       the default of 40 degrees roughly translates to text that is 5 mm tall.
#   dialogMode - true/false.
#       When the dialog mode is activated, no physical printing will occcur. This allows you to test the
#       voice interaction with Alexa without having to wait for things to actually print.
#
# The settings are stored in a file, in JSON format, in a file named 'printerSettings.txt' in the
# same folder as the program.
#
import os
import sys
import json

DefaultSettings = json.loads( '{ "textSize":40, "dialogMode":false }' )
Settings = DefaultSettings

def getDialogMode():
    return Settings["dialogMode"]

def setDialogMode( inDialogMode ):
    global Settings
    Settings["dialogMode"] = inDialogMode

def getTextSize():
    return Settings["textSize"]

def setTextSize( newSize ):
    global Settings
    Settings["textSize"] = newSize

def loadSettings():
    global Settings
    try:
        f = open( "printerSettings.txt", "r" )
    except FileNotFoundError:
        Settings = DefaultSettings
    else:   
        contents = f.read()
        print( contents, file=sys.stderr )
        Settings = json.loads( contents )
        f.close()

def saveSettings():
    contents = json.dumps( Settings )
    print( contents, file=sys.stderr )

    f = open( "printerSettings.txt", "w+" )
    f.write( contents )
    f.close()