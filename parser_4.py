import sys
import sys
def define_symb(file):
    symb=[]
    i=0
    while i<len(file):
        c=file[i]
        if c in [' ', '\n', '\t','\r']:
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
def convert_key(key):
    name=''
    if key.replace('_','').replace('-','').replace('.','').isalnum():
        name=key
    return name
def convert_value(value):
    if type(value)==bool:
        return 'true' if value else 'false'
    return str(value)
def main_convert(obj, lvl=0):
    output=[]
    space=' '*lvl
    for key in obj:
        value=obj[key]
        if type(value)==list:
            items=value
        else:
            items=[value]
        for elem in items:
            if type(elem)==dict:
                output.append(f"{space}<{key}>\n")
                output.append(main_convert(elem,lvl+1))
                output.append(f"{space}</{key}>\n")
            else:
                output.append(f"{space}<{key}>{convert_value(elem)}</{key}>\n")
    return ''.join(output)
f=open("Schedule.hcl")
file=f.read()
f.close()
symb=define_symb(file)
data=parse_file()
xml_doc='<?xml version="1.0" encoding="UTF-8"?>\n'
xml_doc+=f'<root>\n{main_convert(data,1)}</root>\n'
f=open('Schedule.xml','w')
f.write(xml_doc)
print(xml_doc)
    