# keywords for polygons
TRIANGLES = 3
QUADS = 4


# cell height
HEIGHT = 50
COUNT_HEIGHT = 20
# cell padding
PADDING = 20
# min cell width
MIN_WIDTH = 64

# data frame output format
OUTPUT_FORMAT = 'xls'
# default data frame output filename
OUTPUT_FILE_NAME = 'vertices.xlsx'
# default data frame sheet in excel-file
XLS_SHEET_NAME = 'vertices sheet'


# starting dataframe
DATAFRAME0 = {
    'x': [ 1.0,  1.0, -1.0, -1.0,  -1.0, -1.0, -1.0, -1.0,   1.0, -1.0, -1.0,  1.0, ],
    'y': [-1.0, -1.0, -1.0, -1.0,  -1.0, -1.0,  1.0,  1.0,   1.0,  1.0, -1.0, -1.0, ],
    'z': [-1.0,  1.0,  1.0, -1.0,  -1.0,  1.0,  1.0, -1.0,   1.0,  1.0,  1.0,  1.0, ],
    'R': [ 1.0,  1.0,  1.0,  1.0,   0.0,  0.0,  0.0,  0.0,   0.0,  0.0,  0.0,  0.0, ],
    'G': [ 0.0,  0.0,  0.0,  0.0,   1.0,  1.0,  1.0,  1.0,   0.0,  0.0,  0.0,  0.0, ],
    'B': [ 0.0,  0.0,  0.0,  0.0,   0.0,  0.0,  0.0,  0.0,   1.0,  1.0,  1.0,  1.0, ],
    'A': [ 1.0,  1.0,  1.0,  1.0,   1.0,  1.0,  1.0,  1.0,   1.0,  1.0,  1.0,  1.0, ],
}

# empty row for adding to dataframe
NEW_ROW = {
    'x': 0.0,
    'y': 0.0,
    'z': 0.0,
    'R': 1.0,
    'G': 1.0,
    'B': 1.0,
    'A': 1.0,
}

# empty dataframe
EMPTY_DATAFRAME = {
    'x': [ 1.0,  1.0, -1.0, -1.0, ],
    'y': [-1.0, -1.0, -1.0, -1.0, ],
    'z': [-1.0,  1.0,  1.0, -1.0, ],
    'R': [1.0, 1.0, 1.0, 1.0, ],
    'G': [0.0, 0.0, 0.0, 0.0, ],
    'B': [0.0, 0.0, 0.0, 0.0, ],
    'A': [1.0, 1.0, 1.0, 1.0, ],
}
