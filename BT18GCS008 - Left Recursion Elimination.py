'''
Program by: Yash Jain, BT18GCS008.
This program checks the input grammar and eliminates Direct Left Recursion only.
The input should be in a file with the name 'input.txt' without the inverted commas.
Format: Use = sign and | sign to write the grammar. For multiple production, use multiple lines.

Sample Input:
A=ABd|Aa|a
B=Be|b

Sample Output:
A=aA'
B=bB'
A'=BdA'|aA'|epsilon
B'=eB'|epsilon

The output shows the grammar after elimination of Direct Left Recursion.
'''
file1=open("Left Recursion Input.txt", 'r')
lines=file1.readlines()
lines=[i.strip().split('=') for i in lines]
grammar={}
for i in range(len(lines)):
    for j in range(len(lines[i][1])):
        if lines[i][1][j]=='µ':
            lines[i][1]=lines[i][1][:j-1]+'\u03b5'+lines[i][1][j+1:]
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
for i in finalgrammar.items():
    print("%s="%i[0], end='')
    for j in range(len(i[1])):
        if j==len(i[1])-1:
            print("%s"%i[1][j], end='')
        else:    
            print("%s|"%i[1][j], end='')
    print()
