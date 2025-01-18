import csv, math

class Prime:
  primeList = []

  def  __init__(self):
    return

  @classmethod
  def __enter__(self):
    self._genedPrimes = []
    t = 3
    #save generator object
    self.__primeGen = self.__nextPrime()
    for _ in self.__primeGen:
      if t==0:
        break
      else:
        t-=1
      
    return self

  @classmethod
  def __nextPrime(self):
    """
    knock off sieve of Eratosthenes
    """
    c = 0
    with open("primes.csv", "r") as p:
      for x in csv.reader(p,delimiter=",",quotechar="|"):
        for y in x:
          c = int(y)
          self.primeList.append(c)
          yield c
    #continue generating next number
    while True:
      #try next number
      while True:
        c += 2
        if not self.isPrime(c):
          continue
        else:
          break
        #print(c, "c")
      self.primeList.append(c)
      self._genedPrimes.append(c)
      #save progress if program shuts down half way
      if len(self._genedPrimes) > len(str(len(self.primeList)))*3:
        with open("primes.csv", "a") as p:
          for x in self._genedPrimes:
            csv.writer(p).writerow([x])
        self._genedPrimes = []
      yield c
    
  @classmethod
  def __exit__(self,*args):
    with open("primes.csv", "a") as p:
      for x in self._genedPrimes:
        csv.writer(p).writerow([x])
    self._genedPrimes = []
    self.primeList = []
    return

  @classmethod
  def genPrime(cls, times=1)->None:
    current = cls.primeList[-1]
    while times!=0:
      current+=1
      for x in Prime.primeList:
        if current%x==0:
          break
      else:
        Prime.primeList.append(current)
        times-=1
    return

  @staticmethod
  def search(array:list, num:int)->tuple:
    index = (len(array)-len(array)%2)/2
    min = 0
    max = len(array)
    while max>=min:
      mid = (max+min)//2
      if array[mid]==num:
        return (mid,)
      elif array[mid]>num:
        if mid-1 <=min: return (min,max)
        max = mid-1
      elif array[mid]<num:
        if mid+1 >= max: return (min,max)
        min = mid+1
    return(min,max)

  
  @classmethod
  def __getitem__(self, key):
    if isinstance(key, int):
      return self.getPrime(key)
    elif isinstance(key, str):
      pass
      
  @classmethod
  def getPrime(cls,index:int)->int:
    if index>=len(cls.primeList):
      for x in cls.__primeGen:
        if len(cls.primeList)> index:
          break
      #cls.genPrime(times=index-len(cls.primeList)+1)
    return Prime.primeList[index]


  # self.primeList read only
  
  @classmethod
  def isPrime(cls, num)->bool:
    acc=0
    lim = math.sqrt(num)
    while cls.getPrime(acc)<lim:
      #return false if divisible by any prime except itself
      if num%cls.getPrime(acc)==0:
        return False
      acc+=1
    else:
      return True

  @classmethod
  def factorize(cls, num:int)->dict:
    
    if cls.isPrime(num):
      return{num:1}
    res ={}
    index =0
    while num!=1:
      if num%cls.getPrime(index)==0:
        if cls.primeList[index] not in res.keys():
          res[cls.primeList[index]] = 1
        else:
          res[cls.primeList[index]] += 1
        num/=cls.primeList[index]
      else:
        index+=1
    return res
