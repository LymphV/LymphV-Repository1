#将单字符分类
def charToType (c):
    assert (len(c) == 1)
    if c.isalpha(): return 'LETTER'
    if c.isdigit(): return 'DIGIT'
    if c in {' ', '\t', '\n'}: return 'INV'
    if c in {' ', '(', ')', '*', '+', '-', '.',
             '/', ':', ';', '<', '=', '[', ']', ','}:
        return c
    raise Exception('行' + str(r.line) + ': ' + "非法字符 '" + c + "'")

#状态转移矩阵
class Tran:
    def __init__ (self, fileName, resvName):
        with open(fileName) as f:
            cont = f.readlines()
        self.length = int(cont[0])
        self.start = int(cont[1])
        cont = [x.split() for x in cont]
        
        self.end = []
        for x in cont[2]:
            if x.isdigit():
                self.end += [(int(x), None)]
            else:
                self.end[-1] = (self.end[-1][0],x)
        self.end = {x : y for x, y in self.end}
        
        self.edge = {(int(x), y) : int(z) for x, y, z in cont[3:]}
        self.edge[(self.start, 'INV')] = self.start
        self.init()
        
        with open(resvName) as f:
            cont = f.readlines()
        self.reserved = {y for x in cont for y in x.split()}
    
    def init (self):
        self.now = self.start
        self.word = ''
        
    def stop (self):
        if self.now in self.end:
            w = self.word
            type = self.end[self.now]
            self.init()
            if (not type) or type == 'ID' and w in self.reserved:
                return (w.upper(), w)
            return (type, w)
        raise Exception('行' + str(r.line) + ': 词法分析出错')
        
    def tran (self, c):
        e = (self.now, charToType(c))
        if e in self.edge:
            self.now = self.edge[e]
            self.word += '' if charToType(c) == 'INV' else c
            return None
        else: return self.stop()

#源代码字符读取
class Read:
    def __init__ (self, fileName):
        with open(fileName) as f:
            self.cont = f.readlines()
        self.line = 0
        
    def read (self):
        self.line = 0
        for x in self.cont:
            self.line += 1
            for y in x:
                yield y


t = Tran('lexical.in', 'reserved.in')
r = Read('code.snl')

#获取一个词法分析的单词
def read ():
    for c in r.read():
        while 1:
            w = t.tran(c)
            if w: yield w
            else: break
    yield t.stop ()
    yield ('#', '#')
    