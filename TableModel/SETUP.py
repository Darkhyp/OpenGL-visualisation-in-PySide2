import pandas as pd

HEIGHT = 50
COUNT_HEIGHT = 20
PADDING = 20
MIN_WIDTH = 100

XLS_FILE_NAME = 'test.xlsx'
XLS_SHEET_NAME = 'test sheet'


# starting dataframe
DATAFRAME0 = pd.DataFrame(
    {'names': ['Mary', 'Jim', 'John'],
     'integers': [100, 200, 300],
     'texts': ['a', 'b', 'c'],
     'floats': [1.2, 2.5, 5.3]})
# empty row for adding to dataframe
NEW_ROW = {'names': 'new Name', 'integers': 0, 'texts': 'new text', 'floats': 0.0}
# empty dataframe
EMPTY_DATAFRAME = pd.DataFrame(
    {'names': ['new Name'], 'integers': [0], 'texts': ['new text'], 'floats': [0.0]}
)
