#from sort import radix_sort, radix_sort_strings, mergesort
from sort import radix_sort_strings, mergesort, heapsort
from selection import quickselect, selectMOM
from hashtable import HashTable
import csv
import warnings

class Event:
    def __init__(self):
        self.id = None
        self.owner_id = None
        self.creation_date = None
        self.count = None
        self.name = None
        self.content = None
        self.deleted = False

class DataGrid:
    def __init__(self):
        self.df = HashTable(10)
      
    def _invert_order(self, arr):
        return arr[::-1]
    
    def _extractArray(self, df, column):
        arr = []
        count = 0
        for event in df.table:
            if event is not None and event.deleted is False:
                if column == "id":
                    arr.append((event, event.id))
                elif column == "owner_id":
                    arr.append((event, event.owner_id))
                elif column == "creation_date":
                    arr.append((event, event.creation_date))
                elif column == "count":
                    arr.append((event, event.count))
                elif column == "name":
                    arr.append((event, event.name))
                elif column == "content":
                    arr.append((event, event.content))
                count += 1
        return arr, count

    def read_csv(self, file, sep=',', encoding='utf-8'):
        """
        Read a csv file and return a HashTable
        """ 
        with open(file, encoding=encoding) as csv_file:
            # read csv file
            csv_reader = csv.reader(csv_file, delimiter=sep)
            
            # iterate over each row and insert into HashTable
            for row in csv_reader:
                event = Event()
                event.id = int(row[0])
                event.owner_id = str(row[1])
                event.creation_date = str(row[2])
                event.count = int(row[3])
                event.name = str(row[4])
                event.content = str(row[5])
                self.df.insert(event.id, event)

    def show(self, start=0, end=100, returns = True, prints = False):
        """
        If the table has not been sorted yet, it will show the entries between start and end by
        iterating over the items of the HashTable. 
        If the table has been sorted, it will show the entries between start and end of the ordered array.
        """

        try:
            # tries to take the last ordered array
            arr = self.orderedArr
            if end > self.size_arr:
                end = self.size_arr - 1
                warnings.warn("`end` is greater than the size of the datagrid, setting `end` to the datagrid size")
        except:
            arr, size_arr = self._extractArray(self.df, 'id')
            if end > size_arr:
                end = size_arr - 1
                warnings.warn("`end` is greater than the size of the datagrid, setting `end` to the datagrid size")
        
        objects = []
        while start <= end:
            object = self.search("id", arr[start][0].id)
            
            if prints == True and object is not None:
                print(f"{object.id} {object.owner_id} {object.creation_date} {object.count} {object.name} {object.content}")
                objects.append(object)
            elif object is not None:
                objects.append(object)
            else:  
                end += 1

            start += 1
        
        if returns == True:
            return objects

        
    def insert_row(self, row):
        """
        Receives a dictionary and inserts it into the table
        """
        event = Event()
        event.id = int(row["id"])
        event.owner_id = str(row["owner_id"])
        event.creation_date = str(row["creation_date"])
        event.count = int(row["count"])
        event.name = str(row["name"])
        event.content = str(row["content"])
        self.df.insert(event.id, event)

    def delete_row(self, column, value):
        """
        Receives the column and the value to be deleted & deletes
        """
        if column == "position":
            try:
            # tries to take the last ordered array
                arr = self.orderedArr
            except:
                arr, _ = self._extractArray(self.df, 'id')
            
            if type(value) == tuple:
                for i in range(value[0], value[1]+1):
                    self.df.delete("id", arr[i][0].id)
            elif type(value) == int:
                self.df.delete("id", arr[value][0].id)

        else:
            self.df.delete(column, value)
        
    def search(self, column, value):
        """
        Receives the column and the value to be searched & returns 
        every entry accordingly
        """
        objects = self.df.search(column, value)
        return objects

    def sort(self, column, direction='asc'):
        """
        Sorts the table by the column specified
        """
        arr, size_arr = self._extractArray(self.df, column)

        if column=='owner_id' or column=='creation_date':
            arr = radix_sort_strings(arr, len(arr[0]))
                
        if column == 'name':
            arr = radix_sort_strings(arr, 20)
        
        if column == 'id' or column == 'count' or column=='content':
            arr = mergesort(arr)

        if direction=='desc':
            arr = self._invert_order(arr)

        self.orderedArr = arr
        self.size_arr = size_arr

    def select_count(self, i, j, how='median-of-medians'):
        arr, size_arr = self._extractArray(self.df, 'count')
        
        if i > size_arr:
            i = size_arr-1
            warnings.warn("`i` is greater than the size of the datagrid, setting i to size of the datagrid")

        if i < 0:
            i = 0
            warnings.warn("i is less than 0, setting i to 0")
        
        if j > size_arr:
            j = size_arr-1
            warnings.warn("j is greater than the size of the datagrid, setting j the size of the datagrid")

        if how == 'median-of-medians':
            # median-of-medians gives the i-th and j-th smallest values
            i_mom = selectMOM(arr, i)[1]
            j_mom = selectMOM(arr, j)[1]

            entries = []
            count = 0
            for event in arr:
                if event[1] >= i_mom and event[1] <= j_mom:
                    count += 1
                    entries.append((event[0], event[1]))
                if count == j - i + 1:
                    entries = heapsort(entries)
                    break
            
            objects = []

            for event in entries:
                objects.append(event[0])

            return objects

        elif how == 'quickselect':
            i_quick = quickselect(arr, i)[1]
            j_quick = quickselect(arr, j)[1]

            entries = []
            count = 0
            for event in arr:
                if event[1] >= i_quick and event[1] <= j_quick:
                    count += 1
                    entries.append((event[0], event[1]))
                if count == j - i + 1:
                    entries = heapsort(entries)
                    break

            objects = []

            for event in entries:
                objects.append(event[0])

            return objects

        elif how == 'heapsort':
            arr = heapsort(arr)
            objects = []
            for event in arr:
                objects.append(event[0])

            return objects[:j-i+1]