from manager import *
import datetime
from utils import *
t = ContextManager("data")
t.getAllShops()


now = datetime.datetime.date(datetime.datetime.now())
print("unscanned files: ", t.unscannedFiles())
items, errors = t.getUnscannedItems()

print("errors: ", *errors)

print()

dayDirectory = {"level": 0}
def insertIntoDirectory(directory: dict, item: Item):
    level = directory["level"]
    associatedGroup = -1
    match level:
        case 0:
            # year group
            associatedGroup = item.bestBy.year
        case 1:
            # month group
            associatedGroup = item.bestBy.month
        case 2:
            # day group
            associatedGroup = item.bestBy.day
    associatedGroup = "{:0>2}".format(associatedGroup)
    
    if level == 2:
        directory.setdefault(associatedGroup, []).append(item)
        return
    elif associatedGroup not in directory:
        newDirectory = {"level": level+1}
        directory[associatedGroup] = newDirectory
        insertIntoDirectory(newDirectory, item)
        return
    
    insertIntoDirectory(directory[associatedGroup], item)

for i in items:
    insertIntoDirectory(dayDirectory, i)

prettyPrintDict(dayDirectory)


# print("items", *items, sep="\n")
truncatedItems = Iterator(items)\
    .filter(lambda x: x.bestBy >= now)\
    .toList()

# print(*sorted(Iterator(truncatedItems).map(lambda x: f"{x.bestBy.isoformat()} {x.name}")), sep = "\n")
# print(*sorted(truncatedItems,key=lambda entry: entry.bestBy), sep="\n")


print("deleting context", t.__del__())
del t
