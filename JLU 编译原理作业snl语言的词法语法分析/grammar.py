#debug = 0

import lexical

#文法四元式生成
class Grammar:
    def __init__ (self, fileName):
        with open(fileName) as f:
            cont = f.readlines()
        cont = [x.split() for x in cont if x[0].isdigit()]
        self.vn = {x[1] for x in cont if x[1] != '|'} #非终极符集
        self.p = {x : set() for x in self.vn} #产生式集
        self.s = cont[0][1] #开始符
        v = self.s
        if v == '|': raise Exception("文法规定错：" + "开始符寻找失败")
        for x in cont:
            if x[1] != '|':
                v = x[1]
                self.p[v] |= {tuple(x[3:])}
            else:
                self.p[v] |= {tuple(x[2:])}
        self.vt = {z for x in self.p.values() for y in x for z in y} - self.vn #终极符集
        self.fir = {} #首符集
        if len(self.get(self.s)) > 1: raise Exception("文法规定错：" + "开始符有多条产生式")
        
    #得到某非终极符的所有产生式
    def get (self, left):
        assert (left in self.p)
        right = self.p[left]
        return {(left, x) for x in right}
    
    #开始符产生式
    def start (self):
        for t in self.get(self.s):
            return t
    
    #首符计算 return:set
    def first (self, x):
        '''
        ddd = 0
        global debug
        if not debug and x == 'DECLAREPART':
            debug = 1
            ddd = 1
            
        if debug:
            print ('debug:', x, self.fir.get(x, ''))
        '''
        
        if x == '#': return {'#'}
        if x == None: return {None}
        if x == '': return {None}
        if x == (): return {None}
        if x in self.fir and self.fir[x] == set(): 
            raise Exception("文法规定错：" + "首符集创建失败")
        if x in self.fir: return self.fir[x]
        self.fir[x] = set()
        if type(x) == tuple:
            b = True
            for y in x:
                y = self.first(y)
                if None in y:
                    self.fir[x] |= (y - {None})
                else:
                    self.fir[x] |= y
                    b = False
                    break
            if b: self.fir[x] |= {None}
        else:
            if x in self.vt:
                self.fir[x] |= {x}
            elif x in self.vn:
                for y in self.p[x]:
                    self.fir[x] |= self.first(y)
        
        '''
        if debug:
            print ('edg:', x, self.fir[x])
        if ddd:
            debug = 0
            print ('end', x, self.fir[x])
        '''
        return self.fir[x]
            

#项目
class Project(tuple):
    def __init__ (self, t):
        tuple.__init__(t)
        self.a, self.alpha, self.beta, self.lookup = t
    
    #生成产生式
    def produce (self):
        return (self.a, self.alpha + self.beta)
    
    #投影
    def project (self, x):
        if self.beta == () or self.beta[0] != x:
            return None
        return createProject(self.a, self.alpha + (x,), self.beta[1:], self.lookup)
    
    #闭包
    def closure (self):
        if self.beta == () or self.beta[0] in g.vt:
            return set()
        b = self.beta[0]
        lookup = g.first(self.beta[1:] + (self.lookup,))
        return {createProject(b, (), y, z) for x, y in g.get(b) for z in lookup}
    
    def first (self):
        if self.beta == (): return None
        return self.beta[0]
            
def createProject (a, b, c, d):
    return Project((a,b,c,d))
        
#fdebug = open('debug.out', 'w')
    
#项目集
class ProjectSet(set):
    def project (self, x):
        return ProjectSet({y.project(x) for y in self} - {None}).closure()
    
    def closure (self):
        a = self
        while 1:
            
            #fdebug.write('   self:' + str(self) + '\n')
            #fdebug.write('   a:' + str(a) + '\n')
            b = set()
            for x in a: b |= x.closure()
            
            #fdebug.write('   b:' + str(b) + '\n\n')
            if b.issubset(self): break
            a = b
            self |= a
        #fdebug.write ('   end:' + str(self) + '\n\n')
        return self
    
    def first (self):
        return {x.first() for x in self} - {None}
        
#状态机
class StateMachine:
    def __init__ (self):
        x, y = g.start()
        self.sm = [ProjectSet({createProject(x, (), y, '#')}).closure()]
        self.go = {}
        i = 0
        while i < len(self.sm):
            v = self.sm[i].first()
            #fdebug.write ('i: ' + str(i) + '\n')
            for x in v:
                #fdebug.write(' x: ' + x + '\n')
                ps = self.sm[i].project(x)
                if ps:
                    if ps in self.sm:
                        self.go[(i,x)] = self.sm.index(ps)
                    else:
                        self.go[(i,x)] = len(self.sm)
                        self.sm += [ps]
            i += 1
    
#分析表
class Tran:
    def __init__ (self, sm):
        with open('project sets.out', 'w') as f:
            for ind, x in enumerate(sm.sm):
                f.write(str(ind)+'\n')
                for y in x:
                    f.write(str(y) + '\n')
                f.write('\n')
                
        with open('project sets go.out', 'w') as f:
            for x in sm.go.items():
                f.write(str(x)+'\n')
            
    
        self.action = {}
        self.goto = {}
        for i in range(len(sm.sm)):
            for p in sm.sm[i]:
                if p.a == g.s and p.beta == () and p.lookup == '#':
                    k, v = (i,'#'), 'AC'
                    if k in self.action and self.action[k] != v: 
                        raise Exception("文法规定错：" + "非LR(1)文法，" + 
                                        str((k,v)) + "的'AC'项矛盾")
                    self.action[k] = v
                elif p.beta == ():
                    k, v = (i,p.lookup), ('R', p.produce())
                    if k in self.action and self.action[k] != v:
                        raise Exception("文法规定错：" + "非LR(1)文法，" +
                                        str((k,v)) + "项矛盾")
                    self.action[k] = v
                elif p.beta[0] in g.vt:
                    k, v = (i,p.beta[0]), ('S', sm.go[(i, p.beta[0])])
                    if k in self.action and self.action[k] != v:
                        raise Exception("文法规定错：" + "非LR(1)文法，" +
                                        str((k,v)) + "项矛盾")
                    self.action[k] = v
        for i, a in sm.go:
            if a in g.vn:
                self.goto[(i,a)] = sm.go[(i,a)]
        

        with open('action.out', 'w') as f:
            for x in self.action.items():
                f.write(str(x)+'\n')
        
        with open('goto.out', 'w') as f:
            for x in self.goto.items():
                f.write(str(x)+'\n')
                
    
        
                    
            



g = Grammar('grammar.in')
t = Tran(StateMachine())


    
    

#语法分析
def analysis ():
    action = t.action
    goto = t.goto
    state = [0]
    symbol = [('#','#')]
    
    
    f = open ('process.out', 'w')
    def write ():
        f.write ('state : ' + ''.join([str(x) for x in state]) + '\n')
        f.write ('symbol : ' + ','.join([str(x) for x in symbol]) + '\n')
        f.write ('action : ' + str(act) + '\n')
        f.write ('goto : ' + str(go) + '\n')
        f.write ('\n')
    try:
        for a, b in lexical.read():
            while 1:
                sTop = state[-1]
                act = action.get((sTop,a), 'ERR')
                go = ''
                if act == 'ERR':
                    write()
                    raise Exception('行' + str(lexical.r.line) + ': 语法分析出错')
                if act == 'AC':
                    write()
                    break
                if act[0] == 'S':
                    act, go = act
                    write()
                    state += [go]
                    symbol += [(a,b)]
                    break
                if act[0] == 'R':
                    left, right = act[1]
                    lr = len(right)
                    
                    assert (lr < len(state))
                    go = goto.get((state[-1-lr],left), 'ERR')
                    write()
                    if go == 'ERR':
                        raise Exception('行' + str(lexical.r.line) + ': 语法分析出错')
                    l = len(state)
                    state = state[:l-lr] + [go]
                    symbol = symbol[:l-lr] + [left]    
    finally:
        f.close()

#print(g.first(('FIELDDECLIST',)))
