import operator
from functools import reduce
"""
parameters
----------
lis: list<a>
  list of random numbers

outputs
-------
dict<a:int>
  dictionary with "a" as keys and frequency of occurence in "lis" as values

process
-------
1. simplifies "lis" into set
2. loop through set
3. setting into dictionary, values in set and occurence of value in lis
4. return dictionary

examples
--------
>>>pack([])
{}
>>>pack([5])
{5:1}
>>>pack([2,2,3,7])
{2:2, 3:1, 7:1}
>>>pack([(3,5),(4,2),(4)])
{(3,5):1, (4,2):1, (4):1}
"""
pack = lambda lis:{x:lis.count(x) for x in set(lis)}

"""
parameters
----------
array:dict<a:int>
  dictionary with keys of type a and int values

outputs
-------
(dict<a:int>,dict<a:int>)
  a tuple with 2 dictonaries, first dictionary containing keys that have values in "array" divided by 2,
second dictionary containing keys that have odd values associated

process
-------
1. loop thorough "array" checking if value is even
2. if even, add key to first dictionary and divide value by 2
3. loop through "array" checking if value is odd
4. if odd, add key to second dictionary and assign 1 as value
5. return tuple

examples
--------
>>>sep({})
({}, {})
>>>sep({2:2, 5:3, 7:1})
({2:1, 5:1}, {5:1, 7:1})
>>>sep({13:1})
({}, {13:1})
"""
sep = lambda array:({x:array[x]//2 for x in array if array[x]%2==0},{x:1 for x in array if array[x]%2==1})

"""
parameters
----------

outputs
-------

process
-------

examples
--------
"""
twoTrack = lambda func,otherwise=None:(
  (lambda *inp,**inps:(
    otherwise
    if inp[0]==None else
    func(*inp,**inps))
  )
  if not isinstance(func,tuple) else 
  (lambda *inp,**inps:(
    func[1]
    if inp[0]==None else
    func[0](*inp,**inps))
  )
)

combine = lambda funct1: lambda func2: lambda *inp,**inps: funct1(func2(*inp,**inps))

transform = lambda *funcs: reduce(lambda a,b:combine(b)(a),map(twoTrack,funcs))

unfactor = lambda dicti: reduce(operator.add,map(lambda tup:(tup[0]**tup[1]),dicti.items()),0)

toStrVer = lambda pair:f"{unfactor(pair[0])}*root({unfactor(pair[1])})"


factorial1 = lambda number, stop=1: reduce(operator.mul,list(range(stop, number+1)),1)

flatmap = lambda array: sum(array,[])

foldl = lambda opcode: lambda operand: opcode(operand[0],foldl(opcode)(operand[1:]))
