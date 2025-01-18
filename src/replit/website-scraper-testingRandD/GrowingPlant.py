"""
an experiment with visitor, observer, and delegation patterns
DO NOT COPY THIS CODE! BUGs POSSIBLE
"""
import random
from monad import mList, mMaybe


def makeSure(instance, typ):
  if not isinstance(instance, typ):
    raise TypeError("Expected an instance of %s, got %s" % (typ.__name__, type(instance)))

class Visitable:
  def visit(self, visitor:'Visitor'):
    makeSure(visitor, Visitor)
    visitor.visited(self)

class Visitor:
  def visited(self, element:Visitable):
    raise NotImplementedError()

class Observable:
  def __init__(self, observer):
    makeSure(self, Observable)
    makeSure(observer, Observer)
    # print("initalizing observable", type(self).__name__)
    self._observers = [observer]
  
  def add_observer(self, observer:'Observer'):
    makeSure(observer, Observer)
    self._observers.append(observer)
    
  def update(self, *args, **kwargs):
    for obs in self._observers:
      obs.updated(*args, **kwargs)
      
  def getObservers(self):
    return self._observers

class Observer:
  def updated(self, obs:Observable):
    """
    notifies the observer of what actions to be taken
    """
    raise NotImplementedError()

class PlantHostee(Observable):
  def __init__(self, *observer):
    if (l:=len(observer)) > 1 or l < 0:
      raise TypeError("PlantHostee can't have more than one observer")
    if l == 1:
      super(PlantHostee, self).__init__(observer[0])
      self._observer = self._observers[0]
    else:
      self._observer = None
    
  def add_observer(self, observer:Observer):
    if self._observer is None:
      self._observer = observer
    else:
      raise TypeError("PlantHostee can't have more than one observer")

  def replace_observer(self, newObserver:Observer):
    self._observer = newObserver

  def update(self, *args, **kwargs):
    if self._observer is None:
      raise Exception("no observer")
    self._observer.updated(*args, **kwargs)

class PlantElement(Visitable):
  def water(self):
    raise NotImplementedError(f"Not implemented for {type(self).__name__}")
    
  def visit(self, visitor:Visitor):
    makeSure(visitor, Visitor)
    super(PlantElement, self).visit(visitor)
    
  def __str__(self):
    return type(self).__name__

class PlantElementHoster(PlantElement, Observer):
  def __init__(self, *plantElements:PlantElement):
    makeSure(plantElements, (list, tuple))
    self._elementsHosted = list(plantElements)

  def visit(self, visitor:Visitor):
    super(PlantElementHoster, self).visit(visitor)
    copy = self._elementsHosted[::1]  # prevent infinite iteration
    for elem in copy:
      elem.visit(visitor)
  
  def updated(self, operation:str, obs:Observable, *args): # type: ignore
    # there's a reason why there's methods in classes in python, USE THEM DUMMY(endearingly)
    # strong competitor for JDSL
    makeSure(self, PlantElementHoster)
    makeSure(operation, str)
    makeSure(obs, Observable)
    makeSure(args, tuple)
    if operation == "replace":
      self._elementsHosted[self._elementsHosted.index(obs)] = args[0] # type: ignore
      # print("replacing")
    elif operation == "replace with multiple":
      import time
      time.sleep(0.1)
      i = self._elementsHosted.index(obs) # type: ignore
      self._elementsHosted.remove(obs) # type: ignore
      for l in range(len(args[0])):
        self._elementsHosted.insert(i+l, args[0][l])
    elif operation == "delete":
      self._elementsHosted.remove(obs) # type: ignore
    else:
      print("err, what do i do?")
      pass

  def __repr__(self):
    l = (mList(self._elementsHosted)
    .flatmap(lambda a: mList(repr(a).split("\n")))
    .map(lambda a: "│   "+a if a[0] in ("│", "└", "├", " ") else "└───"+a)
        )
    modify = (lambda lis: modifyH(lis))
    modifyH = (lambda lis1: 
                (lambda x1: 
                  mList.just(x1.replace("│", " ", 1)) ** mList.just()  # type: ignore
                  if x1[0] == "│" else
                  mList.just(x1) ** mList.just() # type: ignore
                )
              # if mList is empty, assume end, reurn blanker
              if (x:=lis1.breakUp())[0] == mMaybe(None) else
              # else decide based on what the last thing was
                (lambda res:
                  (lambda lis:
                    mList.just(lis.replace("│", " ", 1)) ** res 
                    if lis[0] == "│" else
                    mList.just(lis) ** res
                  )
                  # if the line below was blank, then return blanker
                  if (x2:=res.breakUp()[0].unwrap())[0] == " " else
                  # else return forker
                  (lambda lis:
                    mList.just(lis.replace("└","├", 1)) ** res
                    if lis[0] in "└" else
                    mList.just(lis) ** res
                  )
                )(modifyH(x[1])(x[0].unwrap()))
              )
    
    l = modify(l)(f"{type(self).__name__}:")
    l = l.toList()
    #l.insert(0, )#⊢─→│|
    return "\n".join(l)
    
    
  
class Leaf(PlantElement, PlantHostee):
  def __init__(self, hoster:PlantElementHoster):
    makeSure(hoster, PlantElementHoster)
    super(Leaf, self).__init__(hoster)
    self._visitCounter = 0

  def water(self):
    pass  # no action needed
  
  def visit(self, visitor):
    super(Leaf, self).visit(visitor)
    self._visitCounter += 1
    if self._visitCounter == 10:
      # wilting mechansim
      self.update("replace with multiple", self, [])
    print("visiting leaf", self._visitCounter)

  def __repr__(self):
    return "Leaf: " + str(10-self._visitCounter)
    
class Shoot(PlantElementHoster, PlantHostee):
  def __init__(self, observer):
    makeSure(self, Shoot)
    makeSure(observer, Observer)
    super(Shoot, self).__init__()
    PlantHostee.__init__(self, observer)
    
  def water(self):
    # print(super().getObservers())
    if (r:=random.randint(0,100)) == 99:
      self.update("replace with multiple", self, [self, Shoot(self._observer)])
    elif 10 <= r < 20:
      self._elementsHosted.append(Shoot(self))
    elif r < 3:
      self._elementsHosted.extend([Leaf(self), Shoot(self), Leaf(self)])
      pass

  def visit(self, visitor):
    super(Shoot, self).visit(visitor)


class Seed(PlantElement, PlantHostee):
  def __init__(self, observer):
    makeSure(observer, Observer)
    super(Seed, self).__init__(observer)
    
  def water(self):
    self.update("replace", self, Shoot(self._observer))
    
  def visit(self, visitor:Visitor):
    super(Seed, self).visit(visitor)

  def __repr__(self):
    return str(self)
  

class Plant(PlantElementHoster): # delegator
  def __init__(self):
    super(Plant, self).__init__(Seed(self)) # hoster init

  def water(self):
    print("nothing happens")
    
  def visit(self, visitor:Visitor):
    super(Plant, self).visit(visitor)
    return None
    """makeSure(visitor, Visitor)
    # prevent infinite iteration
    copy = self._elementsHosted[::1]
    for element in copy:
      element.visit(visitor) # delegation"""



# what a "client" would be able to edit
class LookVisitor(Visitor):
  def __init__(self):
    self._seen = []

  def seen(self, thing:str):
    self._seen.append(thing)
    
  def visited(self, element:PlantElement): # type: ignore
    makeSure(element, PlantElement)
    self.seen(str(element))
    return
    if isinstance(element,Seed):
      self.seen("a seedling")
    elif isinstance(element, Plant):
      self.seen("a Plant")
    else:
      pass
      self.seen(f"something i don't know(might be a {type(element).__name__})")

  def repeat(self):
    print("I've seen:", " and ".join(self._seen))

class WateringVisitor(Visitor):
  def visited(self, element:PlantElement): # type: ignore
    element.water()

print("\nlooking")
p = Plant()
v = LookVisitor()
p.visit(v)
v.repeat()

print("\nwatering")
p.visit(WateringVisitor())
v = LookVisitor()
p.visit(v)
v.repeat()
print(repr(p))


inp = input(": ")
while inp not in ("exit", "quit"):
  if inp == "water" or inp == "":
    print("\nwatering")
    p.visit(WateringVisitor())
    print(repr(p))
  elif inp == "look":
    print("looking")
    v = LookVisitor()
    p.visit(v)
    v.repeat()
    print(repr(p))
  else:
    break
  inp = input(": ")
    
