import math
from functional_programs import twoTrack, pack, sep, combine, transform, unfactor, toStrVer,factorial1
print("Stop clicking the RUN button, use the shell")
quit()
import GrowingPlant
def factor(number):
  res = []
  div = 2
  while number != 1:
    if number % div == 0:
      res.append(int(div))
      number = number / div
      div -= 1
    div += 1
  return res

def prime(number):
    pri = True
    x = 2
    while x <= number ** 0.5:
        if number % x == 0:
            pri = False
            break
        x+=1
    return pri


def factorial(number, stop=1):
  res = 1
  while number>=stop:
    res *= number
    number-=1
  return res

def nPr(options, choices):
  if options<choices: return None
  return factorial(options, options-choices+1)

def nCr(options, choices):
  return nPr(options,choices)//factorial(choices) # type: ignore

def triangle(*sides,c=0)->None:
  # if not specified
  if not c and len(sides)==2:
    return sides[0]**2+sides[1]**2
  elif c and len(sides)==1:
    return c**2-sides[0]**2
  else:
    return None


def test(func1, func2, *tests):
  for x in tests:
    print(x," equal" if func1(*x)==func2(*x) else f" {func1(*x)}≠{func2(*x)}")

def ans(inp):
  data = {
    
  }
  return data[inp]

def makeDoc(func):
  def parOutAid(inp)->str:
    res = "\n"+inp+"\n"+len(inp)*"-"+"\n"
    userInp = input("\n"+inp.capitalize()+"? ")
    if not userInp:
      res += "None\n"
    while userInp:
      res += userInp
      userInp = input("Type? ")
      res += ": "+userInp+"\n" if userInp else "\n"
        
      userInp = input("Description? ")
      if userInp:
        res += "  "+userInp+"\n"
      if inp == "output": break
      userInp = input("\n"+inp.capitalize()+"?")
    return res
  
  def processes()->str:
    res = "\nprocess\n-------\n"
    step = 1
    userInp = input("\nprocess\nstep"+str(step)+"? ")
    if not userInp:
      res += "None\n"
    while userInp:
      res += str(step)+". "+userInp+"\n"
      step += 1
      userInp = input("\nstep"+str(step)+"? ")
    return res
  
  def examples():
    res = "\nexamples\n--------\n"
    userInp = input("\nCase? ")
    if userInp:
      res += ">>>"+func+"("+userInp+")\n"
      exec("res += str("+func+"("+userInp+"))\n")
    else:
      res += "None\n"
    while userInp:
      userInp = input("\nCase? ")
      if userInp:
        res += ">>>"+func+"("+userInp+")\n"
        exec("res += str("+func+"("+userInp+"))\n")
    return res
  
  res = ("\"\"\""
  + parOutAid("parameters")
  + parOutAid("output")
  + processes()
  + examples()
  + "\"\"\"")
  print(res)
  return res

"""
# test(factorial,factorial1,*[(x,y) for x in range(20) for y in range(20) if y<x])
print("ncr"+str(nCr(8,5)))

print(twoTrack(triangle)(3,4))


print(transform((triangle,0),factor,pack,sep,toStrVer)(5,12))
print(combine(combine(toStrVer)(sep))(combine(pack)(factor))(75.0))
print(sep(pack(factor(75.0))))
num = [2173, 22461359,1373]
for x in num:
  print(factor(x))
  print(prime(x))
  print()
"""