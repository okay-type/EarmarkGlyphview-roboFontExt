from AppKit import NSApp
import mojo.drawingTools as ctx
from mojo.events import addObserver, removeObserver
from mojo.canvas import CanvasGroup
from mojo.UI import CurrentGlyphWindow
from vanilla import Window


# version 1.0.0
# ok@yty.pe

# debug adds an window to remove the observers it helps when testing but you still need to close and open a new glyph window
debug = False

# size of mark flag
s = 66


class MarkyMark(object):

    def __init__(self):
        self.windowname = 'debug window ui test'
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
        addObserver(self, "observerGlyphWindowWillOpen", "glyphWindowWillOpen")
        addObserver(self, "observerDraw", "draw")
        addObserver(self, "observerDrawPreview", "drawPreview")

    def windowClose(self, sender):
        removeObserver(self, "glyphWindowWillOpen")
        removeObserver(self, "draw")
        removeObserver(self, "drawPreview")

    def observerGlyphWindowWillOpen(self, notification):
        self.window = notification["window"]
        self.markview = CanvasGroup((-s, 0, s, s), delegate=CanvasStuff(self.window))
        self.window.addGlyphEditorSubview(self.markview)

    def observerDraw(self, notification):
        if self.markview:
            self.markview.show(True)

    def observerDrawPreview(self, notification):
        # hide the view in Preview mode
        if self.markview:
            self.markview.show(False)


class CanvasStuff(object):
    def __init__(self, w):
        self.window = w
    def opaque(self):
        return False
    def acceptsFirstResponder(self):
        return False
    def acceptsMouseMoved(self):
        return True
    def becomeFirstResponder(self):
        return False
    def resignFirstResponder(self):
        return False
    def shouldDrawBackground(self):
        return False
    def draw(self):
        glyph = self.window.getGlyph()
        if glyph is None:
            return
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

