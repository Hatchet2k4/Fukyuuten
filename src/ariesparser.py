"""TO DO:
   * Work on pretty-printing.
   * Base64/zlib support.
   * Allow escaped characters.
   * Syntax validation.
"""


class NodeList(list):

    def __getitem__(self, key):
        if isinstance(key, basestring):
            for child in self:
                if child.name == key:
                    return child
                # Why? O_O
                """if isinstance(child, Node) and child.name == key:
                    if len(child) > 1:
                        return NodeList(child)
                    return child[0]"""
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
        return children

    def addChild(self, child):
        self.append(child)
        return self


class Node(NodeList):

    def __init__(self, name):
        super(Node, self).__init__()
        self.name = name

    def toDict(self, flat=True):
        if flat:
            result = {}
            for child in self:
                if hasattr(child, 'name'):
                    result[child.name] = child
            return result
        else:
            if len(self) == 1 and not isinstance(self[0], Node):
                # A single non-Node value: leaf node
                result = self[0]

            else:
                # recursively grab all child nodes.  Dictify them
                result = {}
                for child in self:
                    if hasattr(child, 'name') and hasattr(child, 'toDict'):
                        result[child.name] = child.toDict(flat)
                    else:
                        # character data

                        # Make up a key name so it fits in a dict
                        bs_keyname = 'cdata'
                        while bs_keyname in result:
                            bs_keyname += '_'

                        result[bs_keyname] = child

            return result
        """
        if flat:
            # TODO: refactor into something slightly less opaque.
            return dict(zip(
                [n.name for n in self], [None or n[0] for n in self]
            ))
        return {self.name: [getattr(n, "toDict", lambda: n)() for n in self]}
        #"""

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

    def peek(self, symbol):
        return self.source[self._pos:self._pos + len(symbol)] == symbol

    def _grab(self, symbols):
        o = []
        for symbol in symbols:
            n = self.source[self._pos:].find(symbol)
            if n == -1:
                n = len(self.source)
            o.append(n + len(symbol) - 1)
        return min(o)

    def _grabComment(self):
        old = self._pos
        self._pos += self._grab(['--)']) + 1
        return self.source[old:self._pos]

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
            if c == '(':
                if self.peek('--'):
                    self._grabComment()
                else:
                    newNode = Node(self._grabIdentifier())
                    L[-1].addChild(newNode)
                    L.append(newNode)
            elif c == ')':
                assert len(L) > 1, \
                    'Malformed markup document: mismatched end parenthesis.'
                L.pop()
            elif not c.isspace():
                L[-1].addChild(c + self._grabString().rstrip())
        return root
