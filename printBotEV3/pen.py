#
# Module: Pen
# This file contains all the code for handling the pen.
# This includes the raising and lower the pen, and positioning the pen on the page.
#
import os
import sys
import time
import logging
import threading

from ev3dev2.led import Leds
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveTank, SpeedPercent, MediumMotor, LargeMotor
from ev3dev2.button import Button
from ev3dev2.sensor import INPUT_4
from ev3dev2.sensor.lego import ColorSensor

# The line width is the full horizontal range of the carraige. You could make it smaller if you want.
LineWidth = 1050

# The default page height is based on a half sheet of 8.5x11 inch paper.
PageHeight = -1450

# Define some metrics for tracking the pen position and the default motor speeds.
CenterPosition = LineWidth / 2
CurrentPositionX = CenterPosition
CurrentPositionY = 0
PrintSpeedPercent = 20
MotorPrintSpeed = SpeedPercent( PrintSpeedPercent )
BACKLASH = 10

Calibrating = False
ReadyToPrint = False

btn = Button()

# These functions control the height of the pen on the page. When it is lowered, it will deposit
# ink on the page.
def lowerPen():
    MediumMotor( OUTPUT_C ).on_for_degrees( SpeedPercent(25), -180 )

def raisePen():
    MediumMotor( OUTPUT_C ).on_for_degrees( SpeedPercent(25), 180 )

# These functions move the pen on the page, relative to its current position.
def left( distance ):
    global CurrentPositionX
    LargeMotor( OUTPUT_A ).on_for_degrees( SpeedPercent( -PrintSpeedPercent ), distance )
    CurrentPositionX -= distance

def right( distance ):
    global CurrentPositionX
    LargeMotor( OUTPUT_A ).on_for_degrees( SpeedPercent( PrintSpeedPercent ), distance * 1.05 )
    CurrentPositionX += distance

def down( distance ):
    global CurrentPositionY
    LargeMotor( OUTPUT_B ).on_for_degrees( MotorPrintSpeed, -distance )
    CurrentPositionY -= distance

def up( distance ):
    global CurrentPositionY
    LargeMotor( OUTPUT_B ).on_for_degrees( MotorPrintSpeed, distance )
    CurrentPositionY += distance

def angle( horizontal, vertical ):
    global CurrentPositionX, CurrentPositionY
    speedA = MotorPrintSpeed
    speedB = MotorPrintSpeed
    degrees = abs( horizontal )
    if abs( horizontal ) > abs( vertical ):
        degrees = abs( horizontal )
        speedA = SpeedPercent( PrintSpeedPercent * horizontal / abs( horizontal ) )
        speedB = SpeedPercent( PrintSpeedPercent * vertical / abs( horizontal ) )
    else:
        degrees = abs( vertical )
        speedA = SpeedPercent( PrintSpeedPercent * horizontal / abs( vertical ) )
        speedB = SpeedPercent( PrintSpeedPercent * vertical / abs( vertical ) )
    MoveTank( OUTPUT_A, OUTPUT_B ).on_for_degrees( speedA, speedB, degrees )
    CurrentPositionX += horizontal
    CurrentPositionY += vertical

# This function moves the pen to an absolute horizontal position.
def moveTo( position ):
    global CurrentPositionX
    if CurrentPositionX != position:
        difference = position - CurrentPositionX
        LargeMotor( OUTPUT_A ).on_for_degrees( SpeedPercent(30), difference )
        CurrentPositionX = position
        if position == 0:
            left( BACKLASH )
            right( BACKLASH )

# These functions feed the paper in and out.
def feedPaperIn():
    global CurrentPositionY
    # Only feed the paper in if there is no paper already obscuring
    # the color sensor (reflected intensity should be zero in that case)
    if( ColorSensor( INPUT_4 ).reflected_light_intensity < 2 ):
        paperDetected = False
        LargeMotor( OUTPUT_B ).on( SpeedPercent(-50) )
        while( not paperDetected ):
            time.sleep( 0.1 )
#            print( "Light intensity: {}".format( ColorSensor( INPUT_4 ).reflected_light_intensity ), file=sys.stderr)
            if( ColorSensor( INPUT_4 ).reflected_light_intensity > 1 ):
#                print( "Light intensity: {}".format( ColorSensor( INPUT_4 ).reflected_light_intensity ), file=sys.stderr)
                paperDetected = True

        LargeMotor( OUTPUT_B ).stop()
        LargeMotor( OUTPUT_B ).on_for_degrees( SpeedPercent(50), 100 )
        CurrentPositionY = 0

def feedPaperOut():
    if( ColorSensor( INPUT_4 ).reflected_light_intensity > 1 ):
        LargeMotor( OUTPUT_B ).on( SpeedPercent(50) )
        paperDetected = True
        while( paperDetected ):
            time.sleep( 0.1 )
#            print( "Light intensity: {}".format( ColorSensor( INPUT_4 ).reflected_light_intensity ), file=sys.stderr)
            if( ColorSensor( INPUT_4 ).reflected_light_intensity < 2 ):
#               print( "Light intensity: {}".format( ColorSensor( INPUT_4 ).reflected_light_intensity ), file=sys.stderr)
                paperDetected = False
    
        LargeMotor( OUTPUT_B ).stop()
        LargeMotor( OUTPUT_B ).on_for_degrees( SpeedPercent(50), 300 )

def newSheet():
    print( "Add a new sheet. Press enter when ready." )
    feedPaperOut()
    Leds().set_color( "LEFT", "GREEN" )
    Leds().set_color( "RIGHT", "GREEN" )
    btn.wait_for_pressed( 'enter', 5000 )
    Leds().all_off()
    feedPaperIn()

# These are convenience functions to 'start' and 'finish' printing, setting up the
# pen position appropriately and feeding the paper in/out.
def startPrinting():
    global ReadyToPrint
    if not ReadyToPrint:
        feedPaperIn()
        moveTo( 0 )
        ReadyToPrint = True

def finishPrinting():
    global ReadyToPrint
    if ReadyToPrint:
        moveTo( CenterPosition )
        ReadyToPrint = False
        feedPaperOut()

def carriageReturn():
    moveTo(0)

def isNearRightMargin( inMargin ):
    result = False
    if CurrentPositionX > ( LineWidth - inMargin ):
        result = True
    return result

# These functions handle calibrating the printer.
# Once in calibration mode, pressing the up and down buttons with control the height of the pen.
# Pressing the center button with exit calibration mode.
def sideScrollThread():
    global Calibrating
    while True:
        time.sleep( 0.25 )
        moveTo( 0 )
        if( not Calibrating ):
            break
        time.sleep( 0.25 )
        moveTo( LineWidth )
        if( not Calibrating ):
            break
    moveTo( LineWidth / 2 )

def onButtonUp( state ):
    if state:
        print("Up Button", file=sys.stderr)
        MediumMotor( OUTPUT_C ).on_for_degrees( SpeedPercent(25), 10 )

def onButtonDown( state ):
    if state:
        print("Down Button", file=sys.stderr)
        MediumMotor( OUTPUT_C ).on_for_degrees( SpeedPercent(25), -10 )

def onButtonExit( state ):
    global Calibrating
    if state:
        print("Enter Button", file=sys.stderr)
        Calibrating = False

def calibrate():
    global Calibrating
    Calibrating = True
    feedPaperIn()
    lowerPen()
    threading.Thread( target=sideScrollThread, daemon=True ).start()
    btn.on_up = onButtonUp
    btn.on_down = onButtonDown
    btn.on_enter = onButtonExit
    btn.on_backspace = onButtonExit

    Leds().set_color( "LEFT", "GREEN" )
    Leds().set_color( "RIGHT", "GREEN" )

    while Calibrating:
        btn.process()
        time.sleep(0.1)

    Leds().all_off()

    raisePen()
    feedPaperOut()
