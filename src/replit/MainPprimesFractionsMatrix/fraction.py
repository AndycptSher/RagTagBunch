
# from fastcore import nb_imports\*
from multipledispatch import dispatch
import enum

class fraction:

  @staticmethod
  def hcf(x:int, y:int)->int:
    while(y):
      x, y = y, x % y
    return x

  @staticmethod
  def stripEZeros(number)->str:
    index = -1
    while number[index]=="0":
      index-=1
    index+=1
    
    return number if index==0 else number[:index]

  @staticmethod
  def lack10s(number:float)->int:
    return len(str(number).split(".")[1])

  @dispatch()
  def __init__(self):
    self.numerator = 0
    self.denominator = 1
  
  @dispatch(int)
  def __init__(self, num:int):
    self.numerator = num
    self.denominator = 1

  @dispatch(float)
  def __init__(self, num:float):
    numT = int(num*10**self.lack10s(num))
    denT = 10**self.lack10s(num)
    f = self.hcf(numT,denT)
    self.numerator = int(numT/f)
    self.denominator = int(denT/f)

  @dispatch(object)
  def __init__(self, f):
    if not isinstance(f, fraction): raise TypeError(f"{f.__class__} is not fraction")
    self.numerator = f.numerator
    self.denominator = f.denominator
    
  @dispatch(int, int)
  def __init__(self, numerator, denominator):
    f = self.hcf(numerator, denominator)
    self.numerator = int(numerator/f)
    self.denominator = int(denominator/f)

  def isInt(self)->bool:
    return self.denominator==1

  def __str__(self)->str:
    return str(self.numerator/self.denominator)

  def __repr__(self):
    """
    print("value:",self.numerator/self.denominator)
    print("numerator:", self.numerator)
    print("denominator:", self.denominator)
    print()
    """
    return f"value: {self.numerator/self.denominator} \nnumerator: {self.numerator} \ndenominator: {self.denominator}\n"

  def __abs__(self):
    return fraction(abs(self.numerator),abs(self.denominator))

  def __neg__(self):
    return fraction(-self.numerator, self.denominator)

  def __add__(self,f1):
    if isinstance(f1, (int,float,fraction)):
      f1 = fraction(f1)
      return fraction(self.numerator*abs(f1.denominator)+ f1.numerator*abs(self.denominator), self.denominator*f1.denominator)
    elif isinstance(f1, str):
      return f"({self.numerator}/{self.denominator})"+f1
    else:
      return None

  def __rand__(self, f1):
    if isinstance(f1,str):
      return f1+f"({self.numerator}/{self.denominator})"
    return self.__add__(f1)

  def __sub__(self, f1):
    if isinstance(f1,str):
      return None
    return self.__add__(-f1)

  def __rsub__(self,f1):
    if isinstance(f1,str):
      return None
    return self.__rand__(-f1)

  def __mul__(self, f1):
    if isinstance(f1, (int,float,fraction)):
      f1 = fraction(f1)
      return fraction(self.numerator*f1.numerator, self.denominator*f1.denominator)
    else:
      return None
  def __rmul__(self, f1):
    return self.__mul__(f1)

  def __truediv__(self,f1):
    if isinstance(f1, (int,float, fraction)):
      f1 = fraction(f1)
      return fraction(self.numerator*f1.denominator,self.denominator*f1.numerator)
    return None
  def __rtruediv__(self,f1):
    if isinstance(f1,(int, float, fraction)):
      f1 = fraction(f1)
      return fraction(f1.numerator*self.denominator,f1.denominator*self.numerator)
    else:
      return None