'''
Program by: Yash Jain, BT18GCS008.
This program reads input from a file. Please do not leave any empty lines or spaces.
This program checks whether the grammar entered is Operator Grammar or not.
Please only enter Operator Grammar. This code does not convert NonOperator to Operator Grammar.
After checking, if Operator Grammar, the Operator Precedence Table will be printed out.
Enter the Grammar and the String to be checked in a file with the name 'Operator Precedence Input.txt' without the inverted commas.
Format: Use =, ε, | signs to write the grammar. For multiple production, use multiple lines.
Enter the string to be checked in the last line.

Sample Input:
-------------
E=E^T+E
T=T-A*T|T/A%A
A=i

Sample Output:
--------------
Operator Grammar
Precedence Table:
     $    i    ^    +    -    *    /    %
$  [-]  [<]  [<]  [<]  [<]  [<]  [<]  [<]
i  [>]  [-]  [>]  [>]  [>]  [>]  [>]  [>]
^  [>]  [<]  [>]  [>]  [<]  [<]  [<]  [<]
+  [>]  [<]  [<]  [<]  [<]  [<]  [<]  [<]
-  [>]  [<]  [>]  [>]  [>]  [<]  [<]  [<]
*  [>]  [<]  [>]  [>]  [>]  [<]  [<]  [<]
/  [>]  [<]  [>]  [>]  [>]  [>]  [>]  [<]
%  [>]  [<]  [>]  [>]  [>]  [>]  [>]  [>]
'''
import pandas as pd
def checkGrammar(grammar):
    for i in grammar.values():
        for j in range(len(i)):
            if 'ε' in i[j]:
                return 0
            if len(i[j]) >1:
                for k in range(len(i[j])-1):
                    if not i[j][k].isalpha():
                        continue
                    if str(i[j][k]).islower() != str(i[j][k+1]).isupper():
                        return 1
    return 2
file1=open("E:/UNI/Moodle/Semester 5/Compiler Design/Lab/Operator Precedence/Operator Precedence Input.txt", 'r')
lines=file1.readlines()
lines=[i.strip().split('=') for i in lines]
for i in range(len(lines)):
    while 'Îµ' in lines[i][1]:
        loc=lines[i][1].find('µ')
        lines[i][1]=lines[i][1][:loc-1]+'\u03b5'+lines[i][1][loc+1:]
grammar={i[0]:i[1].split('|') for i in lines}
operatorGrammar=checkGrammar(grammar)
if operatorGrammar==2:
    print("Operator Grammar")
elif operatorGrammar==1:
    print("Can be converted")
elif operatorGrammar==0:
    exit("Not Operator Grammar")
operators={'$':0}
associativity={'$':'-'}
terminals=[j for i in grammar.values() for j in i if j.islower()]
operatorPriority={'+': 2,'-':1, '*':3, '/':4,'%':5, '^':6, '$':0, '(':7, ')':7}
operatorAssociativity={'+': '>','-':'>', '*':'>', '/':'>','%':'>', '^':'<', '$':0,'(':'>', ')':'>'}
for i in terminals:
    operatorPriority[i]=float('inf')
    operatorAssociativity[i]=float('inf')
    operators[i]=float('inf')
    associativity[i]='-'
count=0
for i in grammar.items():
    ls=[]
    for j in range(len(i[1])):
        for k in range(len(i[1][j])):
            if not i[1][j][k].isalpha():
                ls.append(i[1][j][k])
                if k==len(i[1][j])-1 or k==0:
                    print('Error')
                elif i[1][j][k-1]==i[1][j][k+1]:
                    associativity[i[1][j][k]]=operatorAssociativity[i[1][j][k]]
                elif i[1][j][k-1]==i[0]:
                    associativity[i[1][j][k]]='>'
                elif i[1][j][k+1]==i[0]:
                    associativity[i[1][j][k]]='<'
                else:
                    associativity[i[1][j][k]]=operatorAssociativity[i[1][j][k]]
    val=count
    for j in ls:
        operators[j]=count+operatorPriority[j]
        if count+operatorPriority[j] >val:
            val=count+operatorPriority[j]

    count=val
precedence={i: {j:'' for j in operators}for i in operators}
for i in precedence:
    for j in precedence[i]:
        if i==j:
            precedence[i][j]=[associativity[i]]
        elif operators[i]>operators[j]:
            precedence[i][j]=['>']
        elif operators[i]<operators[j]:
            precedence[i][j]=['<']
        
# print(precedence)
row=[]
for i in precedence.items():
    data_row=i[1]
    operator=i[0]
    data_row['Operator']=operator
    row.append(data_row)
precedence_df=pd.DataFrame(row, index=precedence.keys(),columns=operators)
print("Precedence Table:")
print(precedence_df)