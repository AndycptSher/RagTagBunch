

def trimType(path: str) -> str:
    """
	trims the ".???" from the end of a string path
    """

    assert isinstance(path, str), f"trimType recieved {type(path)} instead of str"
    """
    alternative more generic implemetation
    assert (targetIndex := path.rfind(".")) != -1
    return path[:targetIndex]
    """
    return path[:-4]

def readFileToLines(file):
    """
    helper generator function to return lines in a file
    file: opened file object
    """
    while True:
        line = file.readline()
        if line == "": break # if there is an empty line, "\n" returned
        if line == "\n": continue # ignore empty lines
        yield line[:-1]


def toISOFormat(looseFormat:str, delimiter:str, context: str = None) -> str:
    """
    converts from a loose format: 1_10_2024 or 31/1
    delimiter: the seperator
    context: used to fill in "missing" values from incomplete dates
    into 2024-10-01 and 2024-01-31
    """
    seperated = looseFormat.split(delimiter)
    if len(seperated) < 3:
        if context is None:
            context = datetime.date.isoformat(datetime.datetime.now())
        missing = context.split("-")
        missing = missing[:-len(seperated)]
        for _ in range(len(missing)):
            seperated.append(missing.pop())
    assert len(seperated[2]) == 4, "please enter full year, not shortened version"
    return "{:0>4}-{:0>2}-{:0>2}".format(*seperated[::-1])

def splitList(ls: list, condition) -> tuple[list, list]:
    list1 = []
    list2 = []
    for i in ls:
        if condition(i):
            list1.append(i)
        else:
            list2.append(i)
    return list1, list2


def prettyToString(obj):
    match obj:
        case dict():
            return prettyDictToString(obj)
        case list():
            return prettyListToString(obj)
        case _:
            return str(obj)

def prettyListToString(lis: list):
    print("translating list: ", lis)
    results = ["["]
    for i in lis:
        results.append("\n".join(map(lambda x: "\t"+x, (prettyToString(i)+",").split("\n"))))
    results.append("]")
    return "\n".join(results)

def prettyDictToString(dictionary:dict):
    results = ["{"]
    for key in sorted(dictionary.keys()):
        results.append("\n".join(map(lambda x: "\t"+x, f"{str(key)}: {prettyToString(dictionary[key])},".split("\n"))))
    results.append("}")
    return "\n".join(results)
    ...

def prettyPrintDict(dictionary):
    print(prettyDictToString(dictionary))


class Iterator:
    class ConsumedException(Exception):
        """
        exception to indicate Iterator is claimed
        """
        def __init__(self, *args: object) -> None:
            super().__init__("Iterator consumed", *args)

    def __init__(self, iterable):
        self.iterable = iter(iterable)
        self.consumed = False

    def __iter__(self):
        if self.consumed: raise self.ConsumedException()
        self.consumed = True
        def lazy():
            for i in self.iterable:
                yield i
        return lazy()
    
    def toList(self) -> list:
        return [*self.iterable]
    
    def map(self, func) -> 'Iterator':
        if self.consumed: raise self.ConsumedException()
        self.consumed = True
        def lazy():
            for i in self.iterable:
                yield func(i)
        return Iterator(lazy())
    
    def filter(self, func) -> "Iterator":
        if self.consumed: raise self.ConsumedException()
        self.consumed = True
        def lazy():
            for i in self.iterable:
                if func(i): yield i
        return Iterator(lazy())
    
    def scanl(self, func, seed):
        if self.consumed: raise self.ConsumedException()
        self.consumed = True
        def lazy():
            acc = seed
            yield acc
            for i in self.iterable:
                yield (acc := func(acc, i))
        return Iterator(lazy())
    
    def scanl1(self, func):
        if self.consumed: raise self.ConsumedException()
        self.consumed = True
        def lazy():
            iterable = iter(self.iterable)
            acc = next(iterable)
            for i in iterable:
                yield acc
                acc = func(acc, i)
            yield acc
        return Iterator(lazy())
    
    def last(self):
        """
        returns the last element of the iterator
        Warning: may never terminate on infinite iterators
        """
        if self.consumed: raise self.ConsumedException()
        self.consumed = True
        for i in self.iterable:
            pass
        return i
    
    def take(self, num: int) -> 'Iterator':
        if self.consumed: raise self.ConsumedException()
        self.consumed = True
        def lazy():
            iterator = iter(self.iterable)
            for _ in range(num):
                yield next(iterator)
        return Iterator(lazy())