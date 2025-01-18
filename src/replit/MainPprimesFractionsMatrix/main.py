from P import Prime
from fraction import fraction




def test():
  with Prime() as prime:
    print(prime.primeList)
    print(prime.factorize(101))
    print(prime.factorize(110480986))
    print(prime.factorize(1929375))
    print(prime.primeList)
    prime.genPrime()
    print(prime.primeList)
    print(prime.getPrime(5))
    print(prime.factorize(143))
    print(prime.factorize(133))
    print(prime.isPrime(400457))
    print(prime.primeList)
    print(prime.getPrime(10223))
    print(prime.search(prime.primeList,10223))
    13355024, 1279

def testFrac():
  tofractions = lambda x:(
list(map(lambda a:
           fraction(a[0],a[1]) if isinstance(a,tuple) else a,x)))
  
  x = [((4),16),(1,3),(5,7),(1,28)]
  x = tofractions(x)
  [print(y.__repr__()) for y in x]

  import operator
  from functools import reduce
  print(reduce(operator.add, x).__repr__())


print("FIX!!!\n", fraction(-0.04166666666666).__repr__())

def gui():
  with Prime() as p:
    inp = "sup"
    while inp != "":
      inp = input("\nwut u want?")
      if inp == "factor":
        while (not inp.isdigit()):
          inp = input("num?")
        print(f"factors of {inp} are {p.factorize(int(inp))}")
  
      elif inp == "checkis":
        while not inp.isdigit():
          inp = input("num?")
        t = "" if p.isPrime(int(inp)) else "not"
        print(inp+f" is {t} a prime")
      elif inp == "run":
        asyncio.run(asyncplayground())
  
import asyncio, time
  
async def asyncplayground():
  async def tim(sec):
    print(index)
    await asyncio.sleep(sec)
    return index
  with Prime() as p:
    print("yo")
    prime = p.__getitem__(0)
    index = 0
    t = time.time()
    pI = 0
    # print(p.factorize(39843319*39843347))
    while prime < 10**11:
      prime = p.getPrime(index)
      if time.time()-t >10:
        print(str(index)+ f", generated at {(index-pI)/(time.time()-t)} primes per second")
        t = time.time()
        pI = index
      index += 1

def nPr(n,r):
  """
  n: list of str ints
  r: len str
  """
  if r==0 or len(n)==0:
    yield ""
  else:
    for x in n:
      t = n.copy()
      t.remove(x)
      for y in nPr(t, r-1):
        yield x+y
      
import time, itertools
def oxbridge():
  with Prime() as prime:
    maxIn = 50000
    while True:
      for x in itertools.combinations(list(range(maxIn+1)),5):
        #print(type(x))
        primes = [prime.getPrime(int(y)) for y in x]
        print(primes)
        isValid = True
        # checks
        for x in primes:
          for y in primes:
            if (x == y):
              continue
            if not prime.isPrime(int(str(x)+str(y))) or not prime.isPrime(int(str(y)+str(x))):
              isValid = False
              break
          if not isValid:
            break
          print(primes)
          time.sleep(10)

from functools import reduce
from itertools import product
def ritangle():
  pass

import matrix

if __name__ == "__main__":
  test()
  quit()
  ritangle()
  quit()
  oxbridge()
  
  

  

  