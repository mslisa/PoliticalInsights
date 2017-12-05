# script for importing data and 

import csv
from PI_app import models

class importer():
    
    def __init__(self):
        error_list = []

    def csv(self, path_to_file, delete_current_files=True, *args):
        # Clear out the data in the model
        if delete_current_files:
            models.Effectiveness.objects.all().delete()

        with open(path_to_file, 'rb') as file_in:
            file_reader = csv.reader(file_in)
            file_headers = file_reader.next()
            # replace header == id with rep_id
            file_headers == ['rep_id' if i == 'id' else i for i in file_headers]
            for row in file_reader:
                # row_types = [str, int, int]
                # converted_row = [t(x) for t,x in zip(row_types, row)]
                row_dict = dict(zip(file_headers, row))
                #Foo(fieldname1=line[1], fieldname2=line[2] ... etc. )
                # can we use list comprehensions to do this?
                new_data = models.Effectiveness(**row_dict)
                try:
                    new_data.save()
                except:
                    self.error_list.append(row)




if __name__ == "__main__":
    main()
