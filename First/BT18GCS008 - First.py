'''
Program by: Yash Jain, BT18GCS008.
This program reads input from a file.
It removes Direct Left Recursion and prints out the First of all non-terminal symbols.
The input should be in a file with the name 'First Input.txt' without the inverted commas.
Format: Use =, ε, | signs to write the grammar. For multiple production, use multiple lines.

Sample Input:
S=ABa|bCA
A=cBCD|ε
B=CdA|ad
C=eC|ε
D=bsf|a

Sample Output:
Removed Left Recursion from grammar:
E=TR
R=ε|+E
T=FS
S=ε|*T
F=n|(E)

First of each variable:
First(E)={n,(}
First(R)={ε,+}
First(T)={n,(}
First(S)={ε,*}
First(F)={n,(}
'''
file1=open("E:/UNI/Moodle/Semester 5/Compiler Design/Lab/First/First Input.txt", 'r')
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
# print(first)