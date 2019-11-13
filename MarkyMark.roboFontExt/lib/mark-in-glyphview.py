from AppKit import NSApp
import mojo.drawingTools as ctx
from mojo.events import addObserver, removeObserver
from mojo.canvas import CanvasGroup
from mojo.UI import getGlyphViewDisplaySettings
from vanilla import Window
from pprint import pprint

# version 1.4
# ok@yty.pe

# debug adds an window to remove the observers it helps when testing but you still need to close and open a new glyph window
debug = False

# size of mark flag
s = 66
windowViewManger = {}



class MarkyMark(object):

    def __init__(self):
        self.windowname = 'Debug MarkyMark'
        for window in [w for w in NSApp().orderedWindows() if w.isVisible()]:
            if window.title() == self.windowname:
                window.close()
        if debug == True:
            self.widthheight = (250, 50)
            self.w = Window(self.widthheight, self.windowname)
            self.w.bind("close", self.windowClose)
            self.w.open()
        self.view = None

        self.markview = None
        addObserver(self, "observerGlyphWindowDidOpen", "glyphWindowDidOpen")
        addObserver(self, "observerDraw", "draw")
        addObserver(self, "observerDrawPreview", "drawPreview")
        addObserver(self, "removeFromWindowViewManger", "glyphWindowWillClose")

    def windowClose(self, sender):
        removeObserver(self, "glyphWindowDidOpen")
        removeObserver(self, "draw")
        removeObserver(self, "drawPreview")
        removeObserver(self, "glyphWindowWillClose")

    def observerGlyphWindowDidOpen(self, notification):
        self.window = notification["window"]
        xywh = (-s, 0, s, s)
        self.markview = CanvasGroup(xywh, delegate=CanvasStuff(self.window))
        self.window.addGlyphEditorSubview(self.markview)
        # add to windowmanger dictionary
        windowViewManger[self.window] = self.markview

    def observerDraw(self, notification):
        if self.markview:
            self.markview.show(True)

    def observerDrawPreview(self, notification):
        # hide the view in Preview mode
        if self.markview:
            self.markview.show(False)

    # clean up dict when window is closed
    def removeFromWindowViewManger(self, notification):
        del windowViewManger[notification['window']]



class CanvasStuff(object):
    def __init__(self, w):
        self.window = w
    def opaque(self):
        return False
    def acceptsFirstResponder(self):
        return False
    def acceptsMouseMoved(self):
        return False
    def becomeFirstResponder(self):
        return False
    def resignFirstResponder(self):
        return False
    def shouldDrawBackground(self):
        return False
    def draw(self):
        # get glyph
        glyph = self.window.getGlyph()
        if glyph is None:
            return
        # update to shift around for the ruler - thanks, frank
        rulerOffset = 0
        if getGlyphViewDisplaySettings()['Rulers']:
            rulerOffset = 17
        xywh = (-s, rulerOffset, s, s+rulerOffset)
        markview = windowViewManger.get(self.window) # get from dict
        markview.setPosSize(xywh)
        # draw mark colored triangle
        if glyph.markColor:
            r = glyph.markColor.r
            g = glyph.markColor.g
            b = glyph.markColor.b
            a = glyph.markColor.a
        else:
            r = g = b = 0
            a = .1
        x, y, w, h = self.window.getVisibleRect()
        ctx.fill(r,g,b,a)
        ctx.stroke(None)
        ctx.newPath()
        ctx.moveTo((x+s, y+s))
        ctx.lineTo((x+s, y))
        ctx.lineTo((x, y+s))
        ctx.closePath()
        ctx.drawPath()
        ctx.fill(None)



MarkyMark()

