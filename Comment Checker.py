'''
Program by: Yash Jain, BT18GCS008
This program looks for comments in a file.
If comments exist, it then looks for single line and multi line comments.
// represents a single line comment
/*....*/ represents a multiline comment
The code finally displays:
- the number of each type of comment
- the lines in which the comments are
'''
fullFile=open("Comment Checker Input.txt", 'r')
lines=fullFile.readlines()
num_comments=0
singlelines=[]
multilines=[]
multilineContinued=False
containComment=False
for i in range(len(lines)):
#     print(lines[i].split())
    if multilineContinued:
        if '*/' in lines[i]:
            multilineContinued=False
        else:
            continue
    if '//' in lines[i]:
        num_comments+=1
        singlelines.append(i+1)
        containComment=True
    elif '/*' in lines[i]:
        multilines.append(i+1)
        multilineContinued=True
        containComment=True
if containComment==False:
    print("There are no comments")
else:
    print("The number of Single line comments: %d"%(len(singlelines)))
    print("Lines containing Single-line comments:\n", singlelines)
    print("The number of Multi line comments: %d"%(len(multilines)))
    print("Lines containing the start of Multi-line comments:\n", multilines)
    print("Total number of comments:%d"%(len(singlelines)+len(multilines)))