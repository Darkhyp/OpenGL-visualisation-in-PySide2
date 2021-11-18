from V3.SETUP import EMPTY_DATAFRAME, OUTPUT_FILE_NAME, XLS_SHEET_NAME, NEW_ROW, OUTPUT_FORMAT
import pandas as pd


class Data:
    """
    Container for data frame storage
    (maybe it should derive pd.DataFrame class)
    """
    file_name = OUTPUT_FILE_NAME
    sheet_name = XLS_SHEET_NAME
    output_format = OUTPUT_FORMAT

    def __init__(self, data):
        self._data = pd.DataFrame(data)

    # properties
    @property
    def shape(self):
        return self._data.shape

    @property
    def columns(self):
        return self._data.columns

    @property
    def values(self):
        return self._data.values

    def get_data(self, row, column):
        return self._data.iloc[row, column]

    def set_data(self, row, column, value):
        try:
            self._data.iloc[row, column] = type(self._data.iloc[row, column])(value)
        except Exception as e:
            print(e)
            return False
        finally:
            return True

    # action methods
    def new(self):
        # create a new data frame (template from SETUP)
        print("new data")

        # créer un nouveau DataFrame
        self._data = pd.DataFrame(EMPTY_DATAFRAME)

    def load(self):
        # load the data frame (excel format is now only realized)
        if self.output_format == 'xls':
            print(f"load from xls-file ({self.file_name})")

            # open xls file
            try:
                in_file = pd.ExcelFile(self.file_name)
                # extract the needed sheet from loaded xls-file
                self._data = in_file.parse(self.sheet_name)
            except Exception as e:
                print(e)
        else:
            raise Exception("Unknown output format")

    def save(self):
        # save the data frame (excel format is now only realized)
        if self.output_format == 'xls':
            print(f"save to xls-file ({self.file_name})")

            # enregistrer les données dans un fichier Excel
            try:
                out_file = pd.ExcelWriter(self.file_name, engine='openpyxl')
                self._data.to_excel(out_file, sheet_name=self.sheet_name, index=False)
                out_file.save()
                out_file.close()
            except Exception as e:
                print(e)

    def delete_line(self, row_indices):
        # delete selected row(s) in the data frame
        print(f"delete line(s): {row_indices}")
        success = False

        # check if there are selected rows
        if len(row_indices):
            # delete selected rows
            try:
                selected_rows = [self._data.index[i] for i in row_indices]
                self._data = self._data.drop(labels=selected_rows, axis=0)
            except Exception as e:
                print(e)
            finally:
                success = True
        else:
            print('there are no selected row')
        return success

    def add_new_line(self):
        # add new row(s) in the data frame (at the end)
        print("add new row")

        self._data = self._data.append(NEW_ROW, ignore_index=True)
