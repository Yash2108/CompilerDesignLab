import re
'''
Program by: Yash Jain, BT18GCS008
This program takes following types of input:
  - 2 operands with an operator in between.
  - 1 operand followed by ++ or -- operator. In this case, only integer input is considered.
  - 1 operand only
Enter strings within inverted commas. '' or "". Both work.
Any operand other than this would result in either an error or incorrect output.
This program assumes there is no spacing in between operator and operand.
The output will state the operator used and the result of the operation.
'''
def output(ls):
    if ls[1]=='+':
        print("Operator Entered: Addition Operator")
        print("Result: ", ls[0]+ls[2])
    elif ls[1]=='-':
        print("Operator Entered: Subtraction Operator")
        print("Result: ", ls[0]-ls[2])
    elif ls[1]=='*':
        print("Operator Entered: Multiplication Operator")
        print("Result: ", ls[0]*ls[2])
    elif ls[1]=='/':
        print("Operator Entered: Division Operator")
        print("Result: ", ls[0]/ls[2])
    elif ls[1]=='%':
        print("Operator Entered: Modulus Operator")
        print("Result: ", ls[0]%ls[2])
    else:
        print("Invalid Operator")

string=input("Enter: ")

if_int = re.findall("(\d+)([+]|[-]|[*]|[/]|[%])(\d+)", string)
if_str = re.findall("([\']|[\"])([a-zA-Z]+)([\']|[\"])([+]|[-]|[*]|[/]|[%])([\']|[\"])([a-zA-Z]+)([\']|[\"])", string)
if_float = re.findall("(\d+\.\d+)([+]|[-]|[*]|[/]|[%])(\d+\.\d+)", string)
if_only_string=re.findall("([\']|[\"])([a-zA-Z]+)([\']|[\"])", string)
if_only_integer=re.findall("(\d+)", string)
if_only_float=re.findall("(\d+\.\d+)", string)

if len(if_float)!=0:
    print("The operands are Floats")
    output([float(if_float[0][0]), if_float[0][1], float(if_float[0][2])])
elif len(if_int)!=0:
    print(if_int[0])
    print("The operands are Integers")
    output([int(if_int[0][0]), if_int[0][1], int(if_int[0][2])])
elif len(if_str)!=0:
    if if_str[0][3]=='+':
        print("Operator Entered: Addition Operator")
        print("Result: ", if_str[0][1]+if_str[0][5])
    else:
        print("Input received are Strings.")
        print("Invalid Operator")
elif len(if_only_string)!=0:
	print("Input received is a single String")
elif len(if_only_float)!=0:
	print("Input received is Float")
elif len(if_only_integer)!=0:
	print("Input received is Integer")
else:
    print("Invalid Input")