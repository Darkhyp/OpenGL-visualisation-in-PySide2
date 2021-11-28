

class myList(list):

    def __init__(self, data, parent=None):
        super(myList, self).__init__(data)
        self.length = len(self)
        self.parent = parent

    def new(self):
        self.__init__([0], self.parent)

    def print(self):
        print(f'myList = {self}, myList.length = {self.length}, myList.parent = {self.parent}')


lst = list([2, 3, 6])
print(f'lst = {lst}')

mylist = myList([2, 3, 6], 5)
mylist.print()

mylist.new()
mylist.print()


import sys
from V3.SETUP import DATAFRAME0
if "V3.data0" in sys.modules:
    del sys.modules["V3.data0"]
from V3.data0 import Data


data = Data(DATAFRAME0, 34)
print(data)
print(data.application)

data.new()
print(data)
print(data.application)






from pandas import DataFrame

class Data(DataFrame):
    def __init__(self, data, parent=None):
        super(Data, self).__init__(data)
        self.parent = parent

    # action methods
    def new(self):
        self.__init__({'x': [0.0], 'y': [0.0], 'z': [0.0]}, self.parent)

DATAFRAME = {
    'x': [ 1.0,  1.0, -1.0, -1.0 ],
    'y': [-1.0, -1.0, -1.0, -1.0 ],
    'z': [-1.0,  1.0,  1.0, -1.0 ],
}

data = Data(DATAFRAME, 34)
print(data)
print(data.parent)

data.new()
print(data)
print(data.parent)

