from drawBot import *
import simple_svg_parser


class SVGImage:

    def __init__(self, svgPath):
        self.path = svgPath
        self.handler = SVGHandlerDB()
        self.parse()

    def parse(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            self.svg = f.read()
        simple_svg_parser.parse(self.svg, self.handler)

    @property
    def width(self):
        return self.handler.width

    @property
    def height(self):
        return self.handler.height

    def _debug(self):
        print('\n'.join(self.handler._lines))

    def _paths(self):
        return list(zip(self.handler._paths, self.handler._properties))

    def draw(self):
        self.handler.draw()


class SVGHandlerDB:

    paths = []
    properties = []

    def __init__(self):
        self._lines = []
        self._paths = []
        self._properties = []

    def metadata(self, data):
        self.width  = data.get('width',  1000)
        self.height = data.get('height', 1000)

    def beginPath(self):
        self._lines += ['B = BezierPath()']
        self._properties += [[]]
        self._paths += [BezierPath()]

    def moveTo(self, x, y):
        self._lines += ['B.moveTo((%s, -%s))' % (x, y)]
        self._paths[-1].moveTo((x, -y))

    def lineTo(self, x, y):
        self._lines += ['B.lineTo((%s, -%s))' % (x, y)]
        self._paths[-1].lineTo((x, -y))

    def curveTo(self, x1, y1, x2, y2, x3, y3):
        self._lines += ['B.curveTo((%s, -%s), (%s, -%s), (%s, -%s))' % (x1, y1, x2, y2, x3, y3)]
        self._paths[-1].curveTo((x1, -y1), (x2, -y2), (x3, -y3))

    def closePath(self):
        self._lines += ['B.closePath()']
        self._paths[-1].closePath()

    def fill(self, r, g, b, a):
        fillProperties = ['fill(%s, %s, %s, %s)' % (r/255, g/255, b/255, a)]
        self._lines += fillProperties
        self._properties[-1] += fillProperties

    def stroke(self, r, g, b, a, width):
        strokeProperties = [
            'strokeWidth(%s)' % width,
            'stroke(%s, %s, %s, %s)' % (r/255, g/255, b/255, a)
        ]
        self._lines += strokeProperties
        self._properties[-1] += strokeProperties

    def setSize(self):
        size(handler.width, handler.height)

    def draw(self):
        save()
        translate(0, self.height)
        for i, path in enumerate(self._paths):
            with savedState():
                exec('\n'.join(self._properties[i]))
                drawPath(path)
        restore()


if __name__ == '__main__':

    svg = SVGImage('tests2/desert.svg')
    size(svg.width, svg.height)
    svg.draw()
