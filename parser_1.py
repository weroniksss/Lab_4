# value ::= string | number | boolean | array | object
# boolean ::= true | false
# array ::= '[' values ']'
# object ::= '{' key_values '}'
# key_value ::= key '=' value
# string ::= '"' characters '"'
# HCL -> TOML opt.95
import sys
def define_symb(file):
    symb=[]
    i=0
    while i<len(file):
        c=file[i]
        if c in [' ', '\n', '\t']:
            i+=1
        elif c in ['=','}','{']:
            symb.append(c)
            i+=1
        elif c=='"':
            i+=1
            while file[i]!='"':
                c+=file[i]
                i+=1
            if i >= len(file):
                print("ERROR: UNCLOSED STRING")
                sys.exit()
            symb.append(('str', c[1:]))
            i+=1
        elif c.isdigit():
            i+=1
            while i<len(file) and (file[i].isdigit() or file[i]=='.'):
                c+=(file[i])
                i+=1
            if '.' in c:
                symb.append(('num',float(c)))
            else:
                symb.append(('num', int(c)))
            i+=1
        elif c.isalpha():
            i+=1
            while i<len(file) and file[i].isalpha():
                c+=(file[i])
                i+=1
            if c=='true':
                symb.append(('bool', True))
            if c=='false':
                symb.append(('bool', False))
            else:
                print("ERROR: UNIDENTIFIED WORD", c)
                sys.exit()
        else:
            print("ERROR: UNIDENTIFIED SYMBOL", file[i])
            sys.exit()
    return symb
symb=[]
i=0
def parse_key_value(res):
    global i
    key=symb[i]
    if key[0]!='str':
        print('ERROR: KEY MUST CONTAIN ""')
        sys.exit()
    i+=1
    if symb[i]!='=':
        print(f'ERROR: "=" EXPECTED AFTER {key[1]}')
        sys.exit()
    i+=1
    value=parse_value()
    key_1=key[1]
    if key_1 in res:
        if type(res[key_1])!=list:
            res[key_1]=[res[key_1]]
        res[key_1].append(value)
    else:
        res[key_1]=value
 
def parse_value():
    global i
    s=symb[i]
    if s=="{":  
        return parse_object()
    if s[0] =="str" or s[0]=="num" or s[0]=="bool":
        i+=1
        return s[1]
    else:
        print(f'ERROR: VALUE EXPECTED, GOT {s[1]}')
        sys.exit()  

def parse_object():
    global i
    i+=1  
    res = {}
    while symb[i] != "}":
        parse_key_value(res)
    i+=1 
    return res
def parse_file():
    global i
    res = {}
    while i < len(symb):
        parse_key_value(res)
    return res

def output(obj, lvl=0):
    space="  " * lvl
    if type(obj)==dict:
        for key in obj:
            if type(obj[key])==dict or type(obj[key])==list:
                print(f'{space}{key}:')
                output(obj[key], lvl+1)
            else:
                print(f'{space}{key}:{repr(obj[key])}')
    elif type(obj)==list:
        n=1
        for item in obj:
            print(f'{space}[{str(n)}]')
            output(item,lvl+1)
            n+=1
 

f=open("Schedule.hcl")
file=f.read()
f.close()
symb=define_symb(file)
data=parse_file()
output(data) 

        


            
            


