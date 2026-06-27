import sqlite3
import glob
import datetime
from utils import *

__all__ = ["ContextManager", "Item"]


currentDataPath = "data"

class ContextManager:
    LASTSCAN = "dateLastScanned"
    SCANNED = "scannedLogs"
    keys = {
        "dayLast": LASTSCAN,
        "scannedDays": SCANNED
    }

    def __init__(self, dataFile: str):
        """
        dataclass to store context during runtime

        dataFile: the file where the context is stored
        """
        self.closed = False
        self.location = dataFile
        self.dayLastScanned: 'datetime.datetime' = None
        self.scannedDays: list[str] = []
        with open(dataFile+"\context.txt", "r") as context:
            for line in readFileToLines(context):
                # ensure line to be parsed has desired format
                if ":" not in line:
                    continue

                key, contents = line.split(":", 1)
                # if the row contains unknown data, ignore
                if key not in ContextManager.keys.values():
                    continue

                match key:
                    case self.LASTSCAN:
                        self.dayLastScanned = contents
                    case self.SCANNED:
                        self.scannedDays = contents.replace(" ","").split(", ")
                    case _:
                        pass
        database = sqlite3.connect(self.location+"/items.db")
        database = database.cursor()
        database.execute("DROP TABLE IF EXISTS Items")
        database.execute("CREATE TABLE IF NOT EXISTS Items(name TEXT, bestBy TEXT, cost INTEGER, datePurchased TEXT, code INTEGER)")
        database.execute("INSERT INTO Items(name, bestBy, cost, datePurchased, code) VALUES ('yo', 'what', 2, 'ea',-1)")
        print(database.execute("SELECT * FROM sqlite_schema").description)
        print(database.fetchall())
        print()
        print(database.execute("PRAGMA table_info([Items]);").description)
        print(database.fetchall())

    def __del__(self):
        """
        load updated data into context file
        """
        if self.closed: return
        context = open(self.location+"\context.txt", "a")

        print("---", file=context)
        print(self.keys["dayLast"]+": {}".format(datetime.date.today().isoformat()), file=context)
        print("", file=context)
        print(self.keys["scannedDays"]+": {}".format(", ".join(self.scannedDays)), file=context)
        self.closed = True
        

    def getAllShops(self) -> list[str]:
        """
        retrieves all the filepaths in the main data file bar context
        """
        temp = [*map(trimType, glob.glob("*.txt", root_dir=self.location))]
        temp.remove("context")
        return temp

    def unscannedFiles(self) -> list[str]:
        """
        returns list of unscanned log file names
        """
        allShops = set(self.getAllShops())

        return list(allShops.difference(self.scannedDays))
    
    def getUnscannedItems(self) -> tuple[list['Item'], list[Exception]]:
        """
        returns a list of all unscanned items
        """
        openedFiles = []
        def keepingTrack(file):
            openedFiles.append(file)
            return file
        results = [Item.safeFromLine(line, file) 
                   for file in self.unscannedFiles() 
                   for line in readFileToLines(keepingTrack(open("%s/%s.txt"%(self.location, file), "r")))
                   ]
        for file in openedFiles: file.close()
        return splitList(results, lambda i: isinstance(i, Item))
        # items = []
        # for file in self.filterScanned():
        #     with open("%s/%s.txt"%(self.location, file), "r") as itemList:
        #         items += [Item.fromLine(line, file) for line in readFileToLines(itemList)]
        # return items

    def recordItems(self):
        """
        records the unscanned items into the corresponding database
        """
        items: list[Item] = self.getUnscannedItems()

        return



class Item:
    def __init__(self,
                name: str, # name of product
                bestBy: datetime.date, # date of expiry of product
                cost: int, # cost of purchase in pence
                datePurchaced: datetime.date=None, # day of purchase
                code: int=-1 # barcode of product
                ):
        """
        constructor for Item
        not to be used outside of class
        """
        self.name: str = name
        self.bestBy: datetime.date = bestBy
        self.cost: int = cost
        self.datePurchaced: datetime.date = datePurchaced
        self.code: int = code
    
    @classmethod
    def fromLine(cls, line: str, datePurchaced:str=None) -> 'Item':
        """
        constructor used to create item object from string data
        """
        try:
            datePurchaced = None if datePurchaced is None else toISOFormat(datePurchaced, "_")
            tokens = line.split()
            cost = tokens.pop()
            cost = int(float(cost)*100)

            bestBy = tokens.pop()
            # regardless of if it's 1 number or numbers with /
            # toISOFormat doesn't care, it accepts both
            bestBy = datetime.date.fromisoformat(toISOFormat(bestBy, "/", context=datePurchaced))
            
            name = " ".join(tokens)
        except Exception as e:
            raise type(e)(*e.args, f"while parsing {line}")
        return cls(name, bestBy, cost, datetime.date.fromisoformat(datePurchaced))
    
    @classmethod
    def safeFromLine(cls, line: str, datePurchaced:str=None) -> 'Item|Exception':
        """
        a non-failing version of fromLine
        """
        try:
            return cls.fromLine(line, datePurchaced=datePurchaced)
        except Exception as e:
            return e


    def __repr__(self):
        return "Name: {}, \nBest By: {}, Cost: {}, Purchase Date: {}, Barcode: {}\n".format(self.name, self.bestBy.isoformat(), self.cost.__repr__(), self.datePurchaced.__repr__(), self.code.__repr__())




        
    