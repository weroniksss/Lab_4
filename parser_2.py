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

f=open("Schedule.hcl")
file=f.read()
f.close()
symb=define_symb(file)
data=parse_file()
print(data)

#CONVERTER
def convert_value(value):
    if type(value)==bool:
        return 'true' if value else 'false'
    if type(value)==str:
        return convert_str(value)
    if type(value)==list:
        return '['+','.join(convert_value(v) for v in value)+']'
    if type(value)==dict:
        for k in value:
            v=value[k]
            return '{'+','.join(convert_key(k)+'='+convert_value(v))+'}'
    return str(value)
def convert_key(key):
    simp_key = key.replace('_','').replace('-','').isalnum()
    return key if simp_key else convert_str(key)
def convert_str(s):
    s=s.replace('\n','\\n').replace('\t','\\t')
    return '"'+s+'"'
def table(value):
    if type(value)==list and all(type(v)==dict for v in value):
        return len(value)>0
def main_convert(obj, prev=''):
    output=[]
    for key in obj:
        value=obj[key]
        if type(value)!=dict and not table(value):
            output.append((convert_key(key)+'='+convert_value(value)+'\n'))
    for key in obj:
        value=obj[key]
        if prev:
            key_new=prev+'.'+convert_key(key)
        else:
            key_new=convert_key(key)
        if type(value)==dict:
            output.append("\n["+key_new+"]\n")
            output.append(main_convert(value,key_new))
        elif table(value):
            for item in value:
                output.append("\n[["+key_new+"]]\n")
                output.append(main_convert(item,key_new))
    return "".join(output)
f=open("Schedule.hcl")
file=f.read()
f.close()
symb=define_symb(file)
i = 0
data = parse_file()
toml_text = main_convert(data).strip()+"\n"
f=open("Schedule.toml",'w')
f.write(toml_text)
f.close()
print(toml_text)
