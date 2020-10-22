'''
Program by: Yash Jain, BT18GCS008.
This program reads input from a file.
It removes Direct Left Recursion, prints out the First and Follow of all non-terminal symbols.
The input should be in a file with the name 'Follow Input.txt' without the inverted commas.
Format: Use =, ε, | signs to write the grammar. For multiple production, use multiple lines.

Sample Input:
S=ABa|bCA
A=cBCD|ε
B=CdA|ad
C=eC|ε
D=bsf|a

Sample Output:
Removed Left Recursion from grammar:
S=ABa|bCA
A=cBCD|ε
B=CdA|ad
C=eC|ε
D=bsf|a

First of each variable:
First(S)={c,e,d,a,b}
First(A)={c,ε}
First(B)={e,d,a}
First(C)={e,ε}
First(D)={b,a}

Follow of each variable:
Follow(S)={$}
Follow(A)={e,d,a,$,b}
Follow(B)={a,e,b}
Follow(C)={c,$,b,a,d}
Follow(D)={e,d,a,$,b}
'''
file1=open("E:/UNI/Moodle/Semester 5/Compiler Design/Lab/Follow/Follow Input.txt", 'r')
lines=file1.readlines()
lines=[i.strip().split('=') for i in lines]
grammar={}
for i in range(len(lines)):
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
        if j[variable_number] not in finalgrammar.keys():
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
    first[i[0]]=check(i[0], 0)

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
        if symbol in prod:
            if symbol==prodlist[0]:
                continue
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