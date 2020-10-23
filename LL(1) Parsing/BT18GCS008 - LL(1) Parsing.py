'''
Program by: Yash Jain, BT18GCS008.
This program reads input from a file. Please do not leave any empty lines or spaces.
It removes Direct Left Recursion, prints out the First and Follow of all non-terminal symbols,
checks whether Grammar is Parsable. Also prints out the Parsing Table.
The program also checks the input string whether its parsable.
Enter the Grammar and the String to be checked in a file with the name 'LL1 Parsing Input.txt' without the inverted commas.
Format: Use =, ε, | signs to write the grammar. For multiple production, use multiple lines.
Enter the string to be checked in the last line.

Sample Input:
E=TG
G=+TG|ε
T=FS
S=*FS|ε
F=i|(E)
i+i*i

Sample Output:
Removed Left Recursion from grammar:
E=TG
G=+TG|ε
T=FS
S=*FS|ε
F=i|(E)

First of each variable:
First(E)={i,(}
First(G)={+,ε}
First(T)={i,(}
First(S)={*,ε}
First(F)={i,(}

Follow of each variable:
Follow(E)={$,)}
Follow(G)={$,)}
Follow(T)={+,$,)}
Follow(S)={+,$,)}
Follow(F)={*,+,$,)}

Parsing Table:
         (      )        *        +       i      $
E   [E=TG]     []       []       []  [E=TG]     []
G       []  [G=ε]       []  [G=+TG]      []  [G=ε]
T   [T=FS]     []       []       []  [T=FS]     []
S       []  [S=ε]  [S=*FS]    [S=ε]      []  [S=ε]
F  [F=(E)]     []       []       []   [F=i]     []
This grammar is LL(1) Parsable
This string is Parsable!
'''
import pandas as pd
file1=open("E:/UNI/Moodle/Semester 5/Compiler Design/Lab/LL(1) Parsing/LL1 Parsing Input.txt", 'r')
lines=file1.readlines()
lines=[i.strip().split('=') for i in lines]
grammar={}
parseString=lines[len(lines)-1][0]+'$'
lines.remove(lines[len(lines)-1])
for i in range(len(lines)-1):
    if len(lines[i])==1:
        continue
    while 'Îµ' in lines[i][1]:
        loc=lines[i][1].find('µ')
        lines[i][1]=lines[i][1][:loc-1]+'\u03b5'+lines[i][1][loc+1:]
for i in range(len(lines)):
    grammar[lines[i][0]]=[lines[i][1]]
finalgrammar={i: [] for i in grammar.keys()}
temp={i: {'alpha':[], 'beta':[]} for i in grammar.keys()}
for i in grammar.keys():
    count=grammar[i][0].count('|')
    while True:
        if count>0:
            x=grammar[i][0][:grammar[i][0].index('|')]
        else:
            x=grammar[i][0]
        if grammar[i][0][0]==i:
            if x[1:] not in temp[i]['alpha']:
                temp[i]['alpha'].append(x[1:])
            if count<=0:
                grammar[i][0]=grammar[i][0][1:]
        else:
            if x not in temp[i]['beta']:
                temp[i]['beta'].append(x)
        if count<=0:
            break
        grammar[i][0]=grammar[i][0][grammar[i][0].index('|')+1:]
        count=grammar[i][0].count('|')
    if grammar[i][0] not in temp[i]['alpha'] and grammar[i][0] not in temp[i]['beta']:
        temp[i]['beta'].append(grammar[i][0])
    if len(temp[i]['alpha'])!=0:
        finalgrammar[i+"'"]=[j+i+"'" for j in temp[i]['alpha']]
        finalgrammar[i+"'"].append('epsilon')
        finalgrammar[i]=[j+i+"'" for j in temp[i]['beta']]
    else:
        for j in temp[i]['beta']:
            finalgrammar[i].append(j)
print("Removed Left Recursion from grammar:")
for i in finalgrammar.items():
    print("%s="%i[0], end='')
    for j in range(len(i[1])):
        if j==len(i[1])-1:
            print("%s"%i[1][j], end='')
        else:    
            print("%s|"%i[1][j], end='')
    print()
print()
def check(terminal_symbol, variable_number):
    temp=[]
    for j in finalgrammar[terminal_symbol]:
        variable_number=0
        if j[variable_number] not in finalgrammar.keys() and j[variable_number]:
            temp.append(j[0])
        else:
            checked=check(j[0],0)
            # print("Recursing, Checked:%s:"%j[0], checked)
            if 'ε' in checked:
                variable_number+=1
                if j[variable_number] not in finalgrammar.keys():
                    temp2=[j[variable_number]]
                else:
                    temp2=check(j[variable_number],0)
                # print("Found epsilon, Var:%s:, "%j[variable_number], temp2)
                for x in temp2:
                    if x not in checked:
                        checked.append(x)
                if 'ε' not in temp2:
                    checked.remove('ε')
            for x in checked:
                if x not in temp:
                    temp.append(x)
    # print("Var:%s:"%terminal_symbol, temp)
    return temp

first={i: [] for i in finalgrammar.keys()}
for i in finalgrammar.items():
    # print("Checking for: ", i[0])
    val=check(i[0], 0)
    for j in val:
        if j not in first[i[0]]:
            first[i[0]].append(j)

print("First of each variable:")
for i in first.items():
    print("First(%s)={"%i[0], end='')
    for j in range(len(i[1])):
        if j==len(i[1])-1:
            print("%s}"%i[1][j], end='')
        else:    
            print("%s,"%i[1][j], end='')
    print()

follow={i: [] for i in finalgrammar}
follow[list(finalgrammar.keys())[0]].append('$')
print("\nFollow of each variable:")

def find_follow(prodlist, symbol):
    temp1=[]
    for prod in prodlist[1]:
        # if symbol==prodlist[0]:
        #     continue
        while symbol in prod:
            loc=prod.find(symbol)
            if loc!=len(prod)-1:
                if prod[loc+1] not in finalgrammar.keys():
                        temp1.append(prod[loc+1])
                else:
                    temp2=getfirst(prodlist[0], prod, loc+1)
                    for k in temp2:
                        temp1.append(k)
            else:
                if follow[prodlist[0]]==[]:
                    for z in finalgrammar.items():
                        val=find_follow(z, prodlist[0])
                        for k in val:
                            temp1.append(k)
                else:
                    for k in follow[prodlist[0]]:
                        temp1.append(k)
            if loc==len(prod)-1:
                prod=''
            else:
                prod=prod[loc+1:]
                # print(prod)
    return temp1

def getfirst(origin, prod, loc):
    temp=[]
    if loc==len(prod):
        if follow[origin]==[]:
            for z in finalgrammar.items():
                val=find_follow(z, prod[0])
                for k in val:
                    temp.append(k)
        else:
            val=follow[origin]
            for k in val:
                temp.append(k)
        return temp

    symbol=prod[loc]
    if symbol not in finalgrammar.keys():
        temp.append(symbol)
    else:
        val=first[symbol]
        for k in val:
            temp.append(k)
    if 'ε' in temp:
        temp.remove('ε')
        val=getfirst(origin, prod, loc+1)
        for k in val:
            temp.append(k)
    return temp
for i in finalgrammar.items():
    for j in finalgrammar.items():
        # print("Getting follow for:%s from:"%i[0], j)
        receive=find_follow(j, i[0])
        # print("Got follow for %s:"%i[0], receive)
        for k in receive:
            if k not in follow[i[0]]:
                follow[i[0]].append(k)
for i in follow.items():
    print("Follow(%s)={"%i[0], end='')
    for j in range(len(i[1])):
        if j==len(i[1])-1:
            print("%s}"%i[1][j], end='')
        else:    
            print("%s,"%i[1][j], end='')
    print()
terminals=[]
for i in finalgrammar.items():
    for j in i[1]:
        for k in j:
            if k not in finalgrammar.keys() and k not in terminals:
                terminals.append(k)
if 'ε' in terminals:
    terminals.remove('ε')
terminals.sort()
terminals.append('$')

finalgrammar_prod_wise=[]
for i in finalgrammar.items():
    for j in i[1]:
        finalgrammar_prod_wise.append(i[0]+'='+j)
# def retrieveFirst(val):
#     x=first[val]
#     return x
def findFirst(prod):
    temp=[]
    # print('at the beginning',prod[0])
    if prod[0] in terminals or prod=='ε':
        temp.append(prod[0])
    else:
        val=first[prod[0]].copy()
        # print('Inside else',val)
        if 'ε' in val:
            # print(first)
            val.remove('ε')
            # print(first)
            for k in val:
                temp.append(k)
            if len(prod)!=1:
                # print("Going to recurse from%s:"%prod[0], prod[1:])
                val=findFirst(prod[1:])
                # print("Just recursed, ", val)
                for k in val:
                    temp.append(k)
            else:
                temp.append('ε')
        else:
            for k in val:
                temp.append(k)
    return temp
                
first_prod_wise={i: [] for i in finalgrammar_prod_wise}
for i in finalgrammar_prod_wise:
    # print("Checking for: ", i[0])
    production=i.split('=')
    first_prod_wise[i]=findFirst( production[1])
# print(first_prod_wise)
parsing_table={i[0]:{k:[] for k in terminals} for i in finalgrammar.items()}

for i in finalgrammar.items():
    for j in i[1]:
        if j=='ε':
            for k in follow[i[0]]:
                if k=='ε':
                    k='$'
                if i[0]+'='+j not in parsing_table[i[0]][k]:
                    parsing_table[i[0]][k].append(i[0]+'='+j)
        else:
            for k in first_prod_wise[i[0]+'='+j]:
                if k=='ε':
                    k='$'
                if i[0]+'='+j not in parsing_table[i[0]][k]:
                    parsing_table[i[0]][k].append(i[0]+'='+j)
row=[]
for i in parsing_table.items():
    data_row=i[1]
    nonterminal=i[0]
    data_row['Non-Terminal']=nonterminal
    row.append(data_row)
parsing_table_df=pd.DataFrame(row, index=parsing_table.keys(),columns=terminals)
print("\nParsing Table:")
print(parsing_table_df)
notLL1parsable=False
for i in parsing_table_df:
    for j in parsing_table_df[i]:
        if len(j)>1:
            notLL1parsable=True

class Stack:
     def __init__(self):
         self.items = []

     def isNotEmpty(self):
         return self.items != []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def top(self):
         return self.items[len(self.items)-1]
def parseTheString(parseString):
    parseStack=Stack()
    parseStack.push('$')
    parseStack.push(list(finalgrammar.keys())[0])
    lookAheadIndex=0
    parsed=False
    while parseStack.isNotEmpty():
        topVal=parseStack.top()
        lookAheadSymbol=parseString[lookAheadIndex]
        if topVal=='ε':
            parseStack.pop()
        # print("TopVal=%s and Look ahead=%s\Stack,"%(topVal, lookAheadSymbol), len(parseString[lookAheadIndex:]))
        if topVal==lookAheadSymbol=='$':
            parsed=True
            parseStack.pop()
            parsed=True
            break
        elif topVal==lookAheadSymbol!='$':
            lookAheadIndex+=1
            parseStack.pop()
        elif topVal not in terminals:
            if len(parsing_table_df[lookAheadSymbol][topVal])!=0:
                val=parsing_table_df[lookAheadSymbol][topVal][0]
                val=val[val.find('=')+1:]
                parseStack.pop()
                for k in val[::-1]:
                    if k!='ε':
                        parseStack.push(k)
            else:
                parsed=False
                break
        elif topVal=='$' and lookAheadSymbol!='$':
            parsed=False
            break
    return parsed

if notLL1parsable:
    print("This grammar is not LL(1) Parsable")
else:
    print("This grammar is LL(1) Parsable")
    parsable=parseTheString(parseString)
    if parsable:
        print("This string is Parsable!")
    else:
        print("Either there is an error in the table or the string is Not Parsable.")