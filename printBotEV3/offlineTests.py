#!/usr/bin/env python3
#
# This program can be run directly, independent of Alexa, for testing purposes.
# It is useful for running snippets of code to make sure the printer is working correctly.
#
# Some predefined functions already exist to test the paper feeding and printing various things.
#
import os
import sys
import time

from ev3dev2.led import Leds

import pen as p
import text as t
import draw as d
import settings

def testPaperFeed():
    p.feedPaperIn()
    t.lineFeed()
    t.lineFeed()
    t.lineFeed()
    p.newSheet()
    t.lineFeed()
    t.lineFeed()
    t.lineFeed()
    p.feedPaperOut()

def helloWorld():
    p.startPrinting()
    t.printText( "hello world" )
    p.finishPrinting()

def logo( size ):
    p.startPrinting()
    d.ev3Logo( size )
    p.finishPrinting()

def giftTags():
    p.startPrinting()
    recipients = { "mom and dad", "john", "c", "d", "e" }

    for name in recipients:
        print( "Current Y Position: {}".format( p.CurrentPositionY ), file=sys.stderr )
        print( "Gift tag height: {}".format( d.giftTagHeight() ), file=sys.stderr )
        print( "Page height: {}".format( p.PageHeight ), file=sys.stderr )
        if( p.CurrentPositionY - d.giftTagHeight() < p.PageHeight ):
            p.newSheet()
        d.giftTag( name, "o" )

    p.finishPrinting()

if __name__ == '__main__':
    Leds().all_off()
    print("Starting Program", file=sys.stderr)
    settings.loadSettings()
    t.updateMetrics( settings.getTextSize() )

#    logo( 800 )
#    giftTags()

#    p.startPrinting()
#    t.printText( "the quick brown fox jumped over a lazy dog." )
#    p.finishPrinting()

#    testPaperFeed()
#    helloWorld()
#    p.calibrate()
#    time.sleep( 2 )
