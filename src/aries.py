"""TO DO:
   * Work on pretty-printing.
   * Base64/zlib support.
   * Comment parsing.
   * Allow escaped characters.
   * Syntax validation.
"""


class NodeList(list):

    def __getitem__(self, key):
        if isinstance(key, basestring):
            for child in self:
                if isinstance(child, Node) and child.name == key:
                    if len(child) > 1:
                        return NodeList(child)
                    return child[0]
        else:
            return super(NodeList, self).__getitem__(key)

    def get(self, key):
        child = self[key]
        if len(child) == 1:
            return child[0]
        else:
            return child

    def getAll(self, key):
        children = NodeList()
        for child in self:
            if isinstance(child, Node) and child.name == key:
                children.append(child)

    def addChild(self, child):
        self.append(child)
        return self


class Node(NodeList):

    def __init__(self, name):
        super(Node, self).__init__()
        self.name = name

    def toDict(self, flat=True):
        if flat:
            return dict(zip([n.name for n in self], [n[0] for n in self]))
        return {self.name: [getattr(n, "toDict", lambda: n)() for n in self]}

    def __str__(self, indent=0):
        i = '\t' * indent
        if not len(self):
            return '(%s)' % self.name
        elif len(self) == 1 and \
             not isinstance(self[0], Node):
            return '(%s %s)' % (self.name, self[0])
        else:
            children = '\n'
            for child in self:
                children += i + '\t'
                try:
                    children += child.__str__(indent + 1)
                except TypeError:
                    children += str(child)
                children += '\n'
            return '(%s %s%s)' % (self.name, children, i)

    __repr__ = __str__


def writeDict(f, d):
    if isinstance(f, basestring):
        f = file(f, 'wt')
    for key, value in d.iteritems():
        print >> f, '(%s %s)' % (key, value)


class Document(object):

    def __init__(self, source):
        super(Document, self).__init__()
        self._pos = 0
        if isinstance(source, basestring):
            source = open(source)
        self.source = source.read()

    def get(self):
        self._pos += 1
        return self.source[self._pos - 1]

    def _grab(self, symbols):
        o = []
        for s in symbols:
            n = self.source[self._pos:].find(s)
            if n == -1:
                n = len(self.source)
            o.append(n)
        return min(*o)

    def _grabIdentifier(self):
        old = self._pos
        self._pos += self._grab(' \n\t()')
        return self.source[old:self._pos]

    def _grabString(self):
        old = self._pos
        self._pos += self._grab('()')
        return self.source[old:self._pos]

    def process(self):
        root = Node("")
        L = [root]
        while self._pos < len(self.source):
            c = self.get()
            if c.isspace():
                continue
            elif c == '(':
                newNode = Node(self._grabIdentifier())
                L[-1].addChild(newNode)
                L.append(newNode)
            elif c == ')':
                assert len(L) > 1, \
                    'Malformed markup document: mismatched end parenthesis.'
                L.pop()
            else:
                L[-1].addChild(c + self._grabString().rstrip())
        return root


if __name__ == '__main__':
    if True:
        print Document('winter.cfg').process()['FRAME_RATE']
    else:
        L = (
            Node('root').addChild(
                Node('test1').addChild(
                    Node('test2').addChild(
                        Node('what').addChild('kay')
                    ).addChild('wee')
                ).addChild(
                    Node('position').addChild('10')
                ).addChild('text node')
            )
        )
        print L
        print L['test1']['test2'].get('what')
