本程序为snl语言的词法和语法分析程序

因在作业文件给出的snl语言语法规定文本中，未规定注释符'{'、'}'和字符起止符"'"以及保留字'repeat'，
故在本程序中，将字符'{'、'}'、"'"视为非法字符,删除保留字'repeat'

因在作业文件给出的snl语言语法规定文本中，同时出现'low'，'top'，'Low'，'Top'但均只出现一次，故认为
'Low'和'low'，'Top'和'top'分别为同一个非终极符，为防止此类现象再次发生，将全部语法的终极符和非终极符
规范为大写(仅对语法规定的文件进行规范，本程序不在意是否全文使用大写)，但非终极符'Program'和终极符
'PROGRAM'，非终极符'ProcDecpart'和非终极符'ProcDecPart'规范为大写后无差别，故将'Program'替换为
'All'，'ProcDecPart'替换为'ProcDecPartII'后再规范为大写

本程序使用python3实现，开发环境为python3.6.3

运行程序main.py，本程序将从lexical.in中获取词法分析的自动机的状态转换矩阵，
并从reserved.in中获取所有的保留字，从grammar.in获取语法的巴克斯范式表示并生成
LR(1)状态机(其中所有项目集见project sets.out，项目集的GO转换见project sets go.out)
和LR(1)分析表(action表见action.out，goto表见goto.out)，再从code.snl中获取源代码进行词法语法分析,
语法分析过程见process.out

当检测到词法或语法错误时，程序停止，报错，如“行40: 语法分析出错”

当无词法或语法错误时，程序运行成功并结束，提示“程序"code.snl"词法分析、语法分析结束，无词法语法错误”

若本程序在命令行运行失败，提示“[Errno 2] No such file or directory: 'lexical.in'”，请将本程序main.py
所在文件夹调整为命令行的当前文件夹即可令本程序正常运行

in文件格式：
reserved.in:
所有保留字以不可见字符隔开

lexical.in:
第一行为状态机的个数
第二行为状态机的初态
第三行为状态机的终态，其中若某终态生成一类单词，在状态编号后给出
第四行起，为状态转移函数，每行依次为当前状态、输入字符、后继状态

grammar.in:
以‘行号)'开始的行视为文法生成式，缩写的文法以'|'开头，视为使用上一条生成式的左部
所有行号，元语言符号，终极符和非终极符，必须以不可见字符隔开
每行仅接受一条生成式

out文件格式：
project sets.out:
项目集标号
后面每行为该项目集中的一个项目[A->α·β,u]，表示为(A,α,β,u)

project sets go.out:
每行为一条项目集间的有向边ISj = GO(ISi, X)，表示为((i,X),j)

action.out:
每行为一个action边act = action(s,a)，表示为((s,a),act)
act分为'AC'，('S',goto(s,a))，和('R',(产生式左部,产生式右部))三种

goto.out:
每行为一个goto边go = goto(s,A)，表示为((s,A),go)

process.out:
每四行依次为状态栈state，符号栈symbol，操作action，和转移goto



若有其他问题，请联系作者：LymphV QQ 470481777 email 470481777@qq.com