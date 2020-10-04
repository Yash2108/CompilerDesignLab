# import Comment
keywords=["abstract","assert","boolean","break","byte","case","catch","char","class","const","continuedefault",
"do","double","else","enum","extends","final","finally","float","for","goto","if","implements","import","instanceof",
"int","interface","long","native","new","package","private","protected","public","return","short","static","strictfp",
"super","switch","synchronized","this","throw","throws","transient","try","void","volatile","while"]
operators=["+","-","/","*","=","%", "<",">","<=", ">=", "++", "--", "."]
separators=["(",")","[","]","{","}", ";"]
used_keywords=[]
used_operators=[]
used_separators=[]
used_identifiers=[]
used_constants=[]
word=''
def CommentRemover(lines):
    multiline=False
    length=len(lines)
    commentLessFile=[]
    for i in range(length):
        lines[i].strip()
        if multiline:
            if "*/" in lines[i]:
                multiline=False
                commentLessFile.append(lines[i][lines[i].find("*/"):-1])
            continue
        elif "//" in lines[i]:
            continue
        elif "/*" in lines[i]:
            if "*/" in lines[i]:
                continue
            else:
                multiline=True
                continue
        
        singleLine=lines[i]
        if singleLine!="":
            commentLessFile.append(singleLine)
    return commentLessFile    

def checkKeyword(word):
    global keywords
    global used_keywords
    if word in keywords and word not in used_keywords:
        used_keywords.append(word)
        # print("Adding Keyword: ", word)
        return True
    else:
        # print("Didnt add keyword: ", word)
        return False

def checkOperator(word):
    global operators
    global used_operators
    if word in operators:
        if word not in used_operators:
            used_operators.append(word)
            # print("Adding Operator: ", word)
        return True
    else:
        # print("Didnt add Operator: ", word)
        return False

def checkSeparator(word):
    global separators
    global used_separators
    if word in separators:
        if word not in used_separators:
            used_separators.append(word)
            # print("Adding Separator: ", word)
        return True
    else:
        # print("Didnt add Separator: ", word)
        return False

def addInIdentifiers(word):
    global used_identifiers
    if word!='' and word!=' ' and word not in keywords:
        # print("Adding Identifier: ", word)
        used_identifiers.append(word)

fullFile=open("Lexical Analyzer Input.txt", "r")
lines = fullFile.readlines()
lines=CommentRemover(lines)
isCharacter=False
isString=False
charLetter=''
stringWord=''
for i in lines:
    word=''
    for j in i:
        if isCharacter:
            if j=='\'':
                isCharacter=False
                used_constants.append(charLetter)
            else:
                charLetter=j
            continue
        elif isString:
            if j=="\"":
                isString=False
                used_constants.append(stringWord)
            else:
                stringWord+=j
            continue
        if j=='':
            continue
        elif j ==' ':
            if checkKeyword(word)!=True and word not in used_identifiers:
                addInIdentifiers(word)
            word=''
        elif j=='\'':
            isCharacter=True
        elif  j=="\"":
            isString=True
        elif checkOperator(j):
            if checkKeyword(word)!=True and word not in used_identifiers:
                addInIdentifiers(word)
            word=''
        elif checkSeparator(j):
            if checkKeyword(word)!=True and word not in used_identifiers:
                addInIdentifiers(word)
            
            word=''
        else:
            # print("Appending word: ", word)
            word=word+j
            # print("Appended word: ", word)
for i in used_identifiers:
    j=i.replace('.', '', 1)
    if j.isdigit():
        used_constants.append(i)
        used_identifiers.remove(i)
print("Used Keywords: ",used_keywords)
print("Used Identifiers: ",used_identifiers)
print("Used Operators: ",used_operators)
print("Used Separators: ",used_separators)
print("Used Constants: ",used_constants)