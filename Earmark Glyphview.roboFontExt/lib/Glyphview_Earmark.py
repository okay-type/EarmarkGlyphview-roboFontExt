from merz import MerzView
from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber


size = 50

class earMark(Subscriber):

    debug = True

    def build(self):
        self.merzView = MerzView((-size, 0, 0, size))
        
        merzContainer = self.merzView.getMerzContainer()
        self.triangle = merzContainer.appendPathSublayer(
            name='okayType.earMark',
            position=(0, 0)
        )
        pen = self.triangle.getPen()
        pen.moveTo((0, size))
        pen.lineTo((size, size))
        pen.lineTo((size, 0))
        pen.closePath()
                
        self.getGlyphEditor().addGlyphEditorSubview(self.merzView)

    def destroy(self):
        self.getGlyphEditor().removeGlyphEditorSubview(self.merzView)

    def glyphEditorDidSetGlyph(self, info):
        glyph = info['glyph']
        if glyph == None:
            return
        self.setGlyphMarkColor(glyph)

    def glyphEditorGlyphDidChangeInfo(self, info):
        glyph = info['glyph']
        if glyph == None:
            return
        self.setGlyphMarkColor(glyph)

    def setGlyphMarkColor(self, glyph):
        color = glyph.markColor
        if color != None:
            r, g, b, a = color
            color = (r, g, b, a * .9)
        if color == None:
            color = (0, 0, 0, .05)
        self.triangle.setFillColor(color)


registerGlyphEditorSubscriber(earMark)