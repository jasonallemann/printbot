#
# Modele: text
# The code in this file handles all of the printing of text characters.
#
# Currently, only the basic alphabet is implemented.
#
import pen as p

# These define the text metrics that can be used to draw different sized segments
# making up the characters.
QUARTER = 10
HALF = QUARTER * 2
THREE_QUARTERS = QUARTER * 3
FULL = QUARTER * 4
LETTER_SPACING = HALF
LINE_SPACING = HALF

# The function updates the text metrics to reflect the text size passed in.
# It is called on startup and whenever the text size is changed.
def updateMetrics( textSize ):
    global QUARTER, HALF, THREE_QUARTERS, FULL, LETTER_SPACING, LINE_SPACING
    QUARTER = textSize / 4
    HALF = QUARTER * 2
    THREE_QUARTERS = QUARTER * 3
    FULL = QUARTER * 4
    LETTER_SPACING = HALF
    LINE_SPACING = HALF

def lineFeed():
    p.down( FULL + LINE_SPACING )

def printText( inText ):
    for character in inText:
        printChar( character )

def printChar( inChar ):
    if inChar == ':':
        printColon()
    if inChar == '-':
        printDash()
    if inChar == 'a' or inChar == 'A':
        printA()
    if inChar == 'b' or inChar == 'B':
        printB()
    if inChar == 'c' or inChar == 'C':
        printC()
    if inChar == 'd' or inChar == 'D':
        printD()
    if inChar == 'e' or inChar == 'E':
        printE()
    if inChar == 'f' or inChar == 'F':
        printF()
    if inChar == 'g' or inChar == 'G':
        printG()
    if inChar == 'h' or inChar == 'H':
        printH()
    if inChar == 'i' or inChar == 'I':
        printI()
    if inChar == 'j' or inChar == 'J':
        printJ()
    if inChar == 'k' or inChar == 'K':
        printK()
    if inChar == 'l' or inChar == 'L':
        printL()
    if inChar == 'm' or inChar == 'M':
        printM()
    if inChar == 'n' or inChar == 'N':
        printN()
    if inChar == 'o' or inChar == 'O':
        printO()
    if inChar == 'p' or inChar == 'P':
        printP()
    if inChar == 'q' or inChar == 'Q':
        printQ()
    if inChar == 'r' or inChar == 'R':
        printR()
    if inChar == 's' or inChar == 'S':
        printS()
    if inChar == 't' or inChar == 'T':
        printT()
    if inChar == 'u' or inChar == 'U':
        printU()
    if inChar == 'v' or inChar == 'V':
        printV()
    if inChar == 'w' or inChar == 'W':
        printW()
    if inChar == 'x' or inChar == 'X':
        printX()
    if inChar == 'y' or inChar == 'Y':
        printY()
    if inChar == 'z' or inChar == 'Z':
        printZ()
    if inChar == ' ':
        printSpace()

    p.right( LETTER_SPACING )

    if p.isNearRightMargin( FULL ):
        p.carriageReturn()
        lineFeed()

def printColon():
    p.down( QUARTER )
    p.lowerPen()
    p.right( QUARTER )
    p.raisePen()
    p.down( HALF )
    p.lowerPen()
    p.left( QUARTER + p.BACKLASH )
    p.raisePen()
    p.up( THREE_QUARTERS )
    p.right( QUARTER + p.BACKLASH )

def printDash():
    p.down( HALF )
    p.lowerPen()
    p.right( HALF )
    p.raisePen()
    p.up( HALF )

def printA():
    p.down( FULL )
    p.lowerPen()
    p.up( FULL )
    p.right( FULL )
    p.down( FULL )
    p.up( HALF )
    p.left( FULL )
    p.raisePen()
    p.right( FULL )
    p.up( HALF )

def printB():
    p.lowerPen()
    p.down( FULL )
    p.right( THREE_QUARTERS )
    p.angle( QUARTER, QUARTER )
    p.angle( -QUARTER, QUARTER )
    p.left( THREE_QUARTERS )
    p.right( THREE_QUARTERS )
    p.angle( QUARTER, QUARTER )
    p.angle( -QUARTER, QUARTER )
    p.left( THREE_QUARTERS )
    p.raisePen()
    p.right( FULL )

def printC():
    p.right( FULL )
    p.down( FULL )
    p.lowerPen()
    p.left( FULL )
    p.up( FULL )
    p.right( FULL )
    p.raisePen()

def printD():
    p.lowerPen()
    p.down( FULL )
    p.right( HALF )
    p.angle( HALF, HALF )
    p.angle( -HALF, HALF )
    p.left( HALF )
    p.raisePen()
    p.right( FULL )

def printE():
    p.right( FULL )
    p.left( p.BACKLASH )
    p.down( FULL )
    p.lowerPen()
    p.left( FULL )
    p.up( HALF )
    p.right( THREE_QUARTERS )
    p.left( THREE_QUARTERS )
    p.up( HALF )
    p.right( FULL )
    p.raisePen()
    p.right( p.BACKLASH )

def printF():
    p.down( FULL )
    p.lowerPen()
    p.up( HALF )
    p.right( HALF )
    p.left( HALF + p.BACKLASH )
    p.up( HALF )
    p.right( HALF + p.BACKLASH )
    p.raisePen()

def printG():
    p.right( FULL )
    p.down( QUARTER )
    p.lowerPen()
    p.angle( -QUARTER, QUARTER )
    p.left( HALF )
    p.angle( -QUARTER, -QUARTER )
    p.down( HALF )
    p.angle( QUARTER, -QUARTER )
    p.right( HALF )
    p.angle( QUARTER, QUARTER )
    p.up( QUARTER )
    p.left( HALF )
    p.right( HALF )
    p.down( HALF )
    p.raisePen()
    p.up( FULL )

def printH():
    p.lowerPen()
    p.down( FULL )
    p.up( HALF )
    p.right( THREE_QUARTERS )
    p.down( HALF )
    p.up( FULL )
    p.raisePen()

def printI():
    p.lowerPen()
    p.down( FULL )
    p.raisePen()
    p.up( FULL )

def printJ():
    p.right( FULL )
    p.left( p.BACKLASH )
    p.lowerPen()
    p.down( THREE_QUARTERS )
    p.angle( -QUARTER, -QUARTER )
    p.left( HALF )
    p.angle( -QUARTER, QUARTER )
    p.up( QUARTER )
    p.raisePen()
    p.up( HALF )
    p.right( FULL + p.BACKLASH )

def printK():
    p.lowerPen()
    p.down( FULL )
    p.up( HALF )
    p.angle( THREE_QUARTERS, -HALF )
    p.angle( -THREE_QUARTERS, HALF )
    p.angle( THREE_QUARTERS, HALF )
    p.raisePen()

def printL():
    p.lowerPen()
    p.down( FULL )
    p.right( THREE_QUARTERS )
    p.raisePen()
    p.up( FULL )

def printM():
    p.down( FULL )
    p.lowerPen()
    p.up( FULL )
    p.angle( HALF, -HALF )
    p.angle( HALF, HALF )
    p.down( FULL )
    p.raisePen()
    p.up( FULL )

def printN():
    p.down( FULL )
    p.lowerPen()
    p.up( FULL )
    p.angle( FULL, -FULL )
    p.up( FULL )
    p.raisePen()

def printO():
    p.lowerPen()
    p.down(FULL)
    p.right( FULL )
    p.up(FULL)
    p.left(FULL)
    p.raisePen()
    p.right(FULL)

def printP():
    p.down( FULL )
    p.lowerPen()
    p.up( FULL )
    p.right( FULL )
    p.down( HALF )
    p.left( FULL + p.BACKLASH )
    p.raisePen()
    p.up( HALF )
    p.right( FULL + p.BACKLASH )

def printQ():
    p.down( QUARTER )
    p.lowerPen()
    p.down( HALF )
    p.angle( QUARTER, -QUARTER )
    p.right( HALF )
    p.angle( QUARTER, QUARTER )
    p.up( HALF )
    p.angle( -QUARTER, QUARTER )
    p.left( HALF + p.BACKLASH )
    p.angle( -QUARTER, -QUARTER )
    p.raisePen()
    p.right( HALF + p.BACKLASH )
    p.down( QUARTER )
    p.lowerPen()
    p.angle( HALF, -HALF )
    p.raisePen()
    p.up( FULL )

def printR():
    p.down( FULL )
    p.lowerPen()
    p.up( FULL )
    p.right( FULL )
    p.down( HALF )
    p.left( FULL + p.BACKLASH )
    p.right( p.BACKLASH )
    p.angle( FULL, -HALF )
    p.raisePen()
    p.up( FULL )

def printS():
    p.right( FULL )
    p.left( p.BACKLASH )
    p.lowerPen()
    p.left( FULL )
    p.down( HALF )
    p.right( FULL )
    p.down( HALF )
    p.left( FULL )
    p.raisePen()
    p.up( FULL )
    p.right( FULL + p.BACKLASH )

def printT():
    p.lowerPen()
    p.right( FULL )
    p.left( p.BACKLASH + HALF )
    p.down( FULL )
    p.raisePen()
    p.up( FULL )
    p.right( p.BACKLASH + HALF )

def printU():
    p.lowerPen()
    p.down( FULL )
    p.right( FULL )
    p.up( FULL )
    p.raisePen()

def printV():
    p.lowerPen()
    p.angle( HALF, -FULL )
    p.angle( HALF, FULL )
    p.raisePen()

def printW():
    p.lowerPen()
    p.down( FULL )
    p.angle( HALF, HALF )
    p.angle( HALF, -HALF )
    p.up( FULL )
    p.raisePen()

def printX():
    p.lowerPen()
    p.angle( FULL, -FULL )
    p.raisePen()
    p.left( FULL + p.BACKLASH )
    p.lowerPen()
    p.angle( FULL, FULL )
    p.raisePen()
    p.right( p.BACKLASH )

def printY():
    p.lowerPen()
    p.angle( HALF, -HALF )
    p.down( HALF )
    p.up( HALF )
    p.angle( HALF, HALF )
    p.raisePen()

def printZ():
    p.lowerPen()
    p.right( FULL )
    p.angle( -FULL, -FULL )
    p.right( FULL )
    p.raisePen()
    p.up( FULL )

def printSpace():
    if( p.CurrentPositionX != 0 ):
        p.right(FULL)