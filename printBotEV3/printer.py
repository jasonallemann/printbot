#!/usr/bin/env python3
#
# This is the main program that handles communication with Alexa.
#
import os
import sys
import time
import logging
import json
import threading

import text as t
import pen as p
import draw
import settings

from agt import AlexaGadget

from ev3dev2.led import Leds
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveTank, SpeedPercent, MediumMotor, LargeMotor
from ev3dev2.button import Button

# Set the logging level to INFO to see messages from AlexaGadget
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stderr))
logger = logging.getLogger(__name__)

class MindstormsGadget(AlexaGadget):
    def __init__(self):
        super().__init__()

    def on_connected( self, device_addr ):
        logger.info( "{} connected to Echo device".format( self.friendly_name ) )

    def on_disconnected( self, device_addr ):
        logger.info( "{} disconnected from Echo device".format( self.friendly_name ) )

    # Handles the Custom.Mindstorms.Gadget control directive.
    def on_custom_mindstorms_gadget_control( self, directive ):
        try:
            payload = json.loads( directive.payload.decode( "utf-8" ) )
            print( "Control payload: {}".format( payload ), file=sys.stderr )
            controlType = payload["type"]

            if controlType == "print":
                print( "Printing a word." )
                if not settings.getDialogMode():
                    p.startPrinting()
                    t.printText( payload["word"] )
                    p.finishPrinting()

            if controlType == "printList":
                print( "Printing a list." )
                itemList = json.loads(payload["items"])
                if not settings.getDialogMode():
                    p.startPrinting()
                    for item in itemList:
                        draw.listItem( item )
                    p.finishPrinting()

            if controlType == "giftTags":
                print( "Printing gift tags." )
                itemList = json.loads(payload["items"])
                sender = payload["sender"]
                if not settings.getDialogMode():
                    p.startPrinting()

                    for item in itemList:
#                        print( "Current Y Position: {}".format( p.CurrentPositionY ), file=sys.stderr )
#                        print( "Gift tag height: {}".format( draw.giftTagHeight() ), file=sys.stderr )
#                        print( "Page height: {}".format( p.PageHeight ), file=sys.stderr )
                        if( p.CurrentPositionY - draw.giftTagHeight() < p.PageHeight ):
                            p.newSheet()
                        draw.giftTag( item, sender )

                    p.finishPrinting()

            if controlType == "mindstorms":
                print( "Drawing the EV3 logo.")
                if not settings.getDialogMode():
                    p.startPrinting()
                    draw.ev3Logo( 800 )
                    p.finishPrinting()

            if controlType == "calibrate":
                print( "Calibrating the printer.")
                if not settings.getDialogMode():
                    p.calibrate()

            if controlType == "setTextSize":
                print( "Setting the text size.")
                settings.setTextSize( payload["size"] * 8 )
                t.updateMetrics( settings.getTextSize() )
                settings.saveSettings()

            if controlType == "getTextSize":
                print( "Getting the text size." )
                self._send_event( "TextSize", {'size': settings.getTextSize() / 8} )

            if controlType == "dialogMode":
                enable = payload["enable"]
                if enable == "on":
                    print( "Entering dialog mode." )
                    settings.setDialogMode( True )
                else:
                    print( "Exiting dialog mode." )
                    settings.setDialogMode( False )

        except KeyError:
            print( "Missing expected parameters: {}".format( directive ), file=sys.stderr )

    def _send_event(self, name, payload):
        self.send_custom_event( 'Custom.Mindstorms.Gadget', name, payload )

if __name__ == '__main__':
    settings.loadSettings()
   
    gadget = MindstormsGadget()

    os.system('setfont Lat7-Terminus12x6')
    Leds().all_off()

    # Gadget main entry point
    gadget.main()
