import simple_svg_parser


class SVGPen:

    def __init__(self, svgPath, otherPen):
        self.path = svgPath
        self.handler = SVGHandlerRF(otherPen)
        self.parse()

    def parse(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            self.svg = f.read()
        simple_svg_parser.parse(self.svg, self.handler)


class SVGHandlerRF:

    def __init__(self, pen):
        self.pen = pen

    def metadata(self, data):
        self.width  = data.get('width',  1000)
        self.height = data.get('height', 1000)

    def beginPath(self):
        pass

    def moveTo(self, x, y):
        self.pen.moveTo((x, -y+self.height))

    def lineTo(self, x, y):
        self.pen.lineTo((x, -y+self.height))

    def curveTo(self, x1, y1, x2, y2, x3, y3):
        self.pen.curveTo((x1, -y1+self.height), (x2, -y2+self.height), (x3, -y3+self.height))

    def closePath(self):
        self.pen.closePath()

    def fill(self, r, g, b, a):
        pass

    def stroke(self, r, g, b, a, width):
        pass


if __name__ == '__main__':
    
    g = CurrentGlyph()
    g.clear()
    svgPen = SVGPen('tests2/desert.svg', g.getPen())
