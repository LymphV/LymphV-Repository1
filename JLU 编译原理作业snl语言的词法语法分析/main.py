
if __name__ == '__main__':
    
    try:
        import grammar
        grammar.analysis ()
        print ('程序"code.snl"词法分析、语法分析结束，无词法语法错误')
    except Exception as e:
        print (e)
