#
# Module: draw
# The code in this file is responsible for drawing graphics and composite items.
# This currently includes rectangles, line art, the mindstorms ev3 logo and gift tags.
#
import pen as p
import text as t

CardMargin = 60

def rectangle( x, y, width, height ):
    p.carriageReturn()
    p.right( x )
    p.down( y )
    p.lowerPen()
    p.right( width )
    p.down( height )
    p.left( width )
    p.up( height )
    p.raisePen()
    p.carriageReturn()

def cutRectangle( x, y, width, height, corner ):
    cornerX = corner
    cornerY = corner * 3 / 4
    p.moveTo( x + cornerX )
    p.down( y )
    p.lowerPen()
    p.right( width - 2 * cornerX )
    p.angle( cornerX, -cornerY )
    p.down( height - 2 * cornerY )
    p.angle( -cornerX, -cornerY )
    p.left( width - 2 * cornerX )
    p.angle( -cornerX, cornerY )
    p.up( height - 2 * cornerY )
    p.angle( cornerX, cornerY )
    p.raisePen()
    p.carriageReturn()

# The size of the line star is specified in horizontal degrees
def lineStar( position, size ):
    p.moveTo( position )
    p.lowerPen()
    p.up( size * 3 / 4 )
    p.down( size * 6 / 4 )
    p.up( size * 3 / 4 )
    p.left( size )
    p.right( size * 2 )
    p.left( size )
    p.angle( size, size * 3 * 0.7 / 4 )
    p.angle( -size * 2, -size * 6 * 0.7 / 4 )
    p.angle( size, size * 3 * 0.7 / 4 )
    p.angle( size, -size * 3 * 0.7 / 4 )
    p.angle( -size * 2, size * 6 * 0.7 / 4 )
    p.angle( size, -size * 3 * 0.7 / 4 )
    p.raisePen()
    p.carriageReturn()

# Draws the EV3 logo, centered horizontally on the page
# The size must be between 300 and the line width (1050)
def ev3Logo( size ):
    if( size > p.LineWidth ):
        size = p.LineWidth
    if( size < 300 ):
        size = 300

    outsideNotch = size * 6 / 80 * 0.7
    insideNotch = size * 14 / 80 * 0.7
    angle = size * 26 / 80
    outsideCenter = size * 28 / 80
    insideCenter = size * 36 / 80
    flange = size * 22 / 80

    p.carriageReturn()
    p.down( outsideNotch + angle * 0.7 )
    p.right( ( p.LineWidth - size ) / 2 )
    p.lowerPen()

    # Top half
    p.up( outsideNotch )
    p.angle( angle, angle * 0.7 )
    p.right( outsideCenter  )
    p.angle( angle, -angle * 0.7 )
    p.down( outsideNotch )
    p.left( flange )
    p.up( insideNotch )
    p.left( insideCenter )
    p.down( insideNotch )
    p.left( flange )
    
    p.raisePen()
    p.down( outsideNotch )
    p.lowerPen()
    
    # Bottom half
    p.down( outsideNotch )
    p.angle( angle, -angle * 0.7 )
    p.right( outsideCenter )
    p.angle( angle, angle * 0.7 )
    p.up( outsideNotch )
    p.left( flange )
    p.down( insideNotch )
    p.left( insideCenter )
    p.up( insideNotch )
    p.left( flange )

    p.raisePen()
    p.right( size * 3 / 8 )
    p.down( insideNotch / 2 )
    p.lowerPen()
    
    # Inside Box
    p.right( size * 2 / 8 )
    p.up( insideNotch + outsideNotch)
    p.left( size * 2 / 8 )
    p.down( insideNotch + outsideNotch )
    p.raisePen()

def giftTagHeight():
    return t.FULL * 4 + CardMargin + t.LINE_SPACING * 3 + CardMargin

def giftTag( toName, fromName ):
    p.carriageReturn()
    cutRectangle( 0, 0, p.LineWidth, t.FULL * 4 + CardMargin + t.LINE_SPACING * 3, CardMargin )
    p.down( CardMargin / 2 )
    p.right( CardMargin * 2 )
    t.printText( "to" )
    p.carriageReturn()
    t.lineFeed()
    lineStar( p.LineWidth - CardMargin - 70, 70 )
    p.right( CardMargin * 2 )
    t.printText( toName )
    p.carriageReturn()
    t.lineFeed()
    p.right( CardMargin * 3 + 140 )
    t.printText( "from" )
    p.carriageReturn()
    t.lineFeed()
    lineStar( CardMargin + 70, 70 )
    p.right( CardMargin * 3 + 140 )
    t.printText( fromName )
    p.carriageReturn()
    t.lineFeed()
    p.down( CardMargin )

def listItem( item ):
    t.printText( "o " )
    t.printText( item )
    p.carriageReturn()
    t.lineFeed()