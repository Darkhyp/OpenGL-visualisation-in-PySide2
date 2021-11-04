from V3.SETUP import EMPTY_DATAFRAME, OUTPUT_FILE_NAME, XLS_SHEET_NAME, NEW_ROW, OUTPUT_FORMAT
from pandas import DataFrame, ExcelFile, ExcelWriter


class Data(DataFrame):
    file_name = OUTPUT_FILE_NAME
    sheet_name = XLS_SHEET_NAME
    output_format = OUTPUT_FORMAT

    def __init__(self, data, application=None):
        super(Data, self).__init__(data)
        self.application = application

    # action methods
    def new(self):
        print("new data")

        # créer un nouveau DataFrame
        self.__init__(EMPTY_DATAFRAME, self.application)

        # # update application
        # self.application.update_data()

    # def load(self):
    #     if self.output_format == 'xls':
    #         print(f"load from xls-file ({self.file_name})")
    #
    #         # open xls file
    #         in_file = ExcelFile(self.file_name)
    #         # extract the needed sheet from loaded xls-file
    #         self.__init__(in_file.parse(self.sheet_name), self.application)
    #
    #         # update application
    #         self.application.update_data()
    #     else:
    #         raise Exception("Unknown output format")
    #
    # def save(self):
    #     if self.output_format == 'xls':
    #         print(f"save to xls-file ({self.file_name})")
    #
    #         # enregistrer les données dans un fichier Excel
    #         out_file = ExcelWriter(self.file_name, engine='openpyxl')
    #         self.to_excel(out_file, sheet_name=self.sheet_name, index=False)
    #         out_file.save()
    #         out_file.close()
    #
    # def delete_line(self):
    #     print("delete line(s)")
    #
    #     selected_rows = set([self._data.index[i.row()] for i in self.application.window.view.selectedIndexes()])
    #
    #     # check if there are selected rows
    #     if len(selected_rows):
    #         # delete selected rows
    #         try:
    #             self._data = self._data.drop(labels=selected_rows, axis=0)
    #
    #             # update application
    #             self.application.update_data()
    #         except Exception as e:
    #             print(e)
    #     else:
    #         print('there are no selected row')
    #
    # def add_new_line(self):
    #     print("add new row")
    #
    #     self = self.append(NEW_ROW, ignore_index=True)
    #
    #     # update application
    #     self.application.update_data()
