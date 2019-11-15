from AppKit import NSApp
import mojo.drawingTools as ctx
from mojo.events import addObserver, removeObserver
from mojo.canvas import CanvasGroup
from mojo.UI import getGlyphViewDisplaySettings
from vanilla import Window
from mojo.UI import CurrentWindow

# version 1.5
# ok@yty.pe

debug = False

# window manager dictionary
windowViewManger = {}

# flag size
size = 66


class MarkyMark(object):

    def __init__(self):
        # debug manager
        self.windowname = 'Debug MarkyMark'
        for window in [w for w in NSApp().orderedWindows() if w.isVisible()]:
            if window.title() == self.windowname:
                window.close()
        if debug == True:
            self.widthheight = (250, 50)
            self.w = Window(self.widthheight, self.windowname)
            self.w.bind("close", self.windowClose)
            self.w.open()

        # observers
        addObserver(self, "observerGlyphWindowDidOpen", "glyphWindowDidOpen")
        addObserver(self, "removeFromWindowViewManger", "glyphWindowWillClose")
        addObserver(self, 'updateSelfWindow', 'currentGlyphChanged')
        addObserver(self, "observerDraw", "draw")
        addObserver(self, "observerDrawPreview", "drawPreview")


    def windowClose(self, sender):
        removeObserver(self, "glyphWindowDidOpen")
        removeObserver(self, "glyphWindowWillClose")
        removeObserver(self, "currentGlyphChanged")
        removeObserver(self, "draw")
        removeObserver(self, "drawPreview")


    def observerGlyphWindowDidOpen(self, notification):
        self.window = notification["window"]
        xywh = (-size, 0, size, size)
        self.markview = CanvasGroup(xywh, delegate=CanvasStuff(self.window))
        self.window.addGlyphEditorSubview(self.markview)
        # add to windowmanger dictionary
        windowViewManger[self.window] = self.markview


    def removeFromWindowViewManger(self, notification):
        # clean up dict when window is closed
        del windowViewManger[notification['window']]


    def updateSelfWindow(self, notification):
        # set window to the active window
        self.window = CurrentWindow()


    def observerDraw(self, notification):
        markview = windowViewManger.get(self.window)
        if markview is not None:
            markview.show(True)


    def observerDrawPreview(self, notification):
        markview = windowViewManger.get(self.window)
        if markview is not None:
            markview.show(False)




class CanvasStuff(object):
    def __init__(self, window):
        self.w = window
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
        glyph = self.w.getGlyph()
        if glyph is None:
            return
        # update to shift around for the ruler - thanks, frank
        rulerOffset = 0
        if getGlyphViewDisplaySettings()['Rulers']:
            rulerOffset = 17
        xywh = (-size, rulerOffset, size, size+rulerOffset)
        markview = windowViewManger.get(self.w)
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
        x, y, w, h = self.w.getVisibleRect()
        ctx.fill(r,g,b,a)
        ctx.stroke(None)
        ctx.newPath()
        ctx.moveTo((x+size, y+size))
        ctx.lineTo((x+size, y))
        ctx.lineTo((x, y+size))
        ctx.closePath()
        ctx.drawPath()
        ctx.fill(None)




MarkyMark()



