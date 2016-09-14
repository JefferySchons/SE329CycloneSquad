import csv

# Loads file at './index.csv' and loads name and id from file
class CSVIndex:
    def __init__(self):
        self.loaded = 0;
        self.read();
    # end def __init__(self)

    def read(self):
        with open('index.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            self.index = []
            for row in reader:
                self.index.append(row);
        self.loaded = 1
    # end def read(self)

    def write(self):
        with open('index.csv', 'w') as csvfile:
            fieldnames = ['id', 'name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in self.index:
                writer.writerow(row)
    # end def write(self)

    def getIDFromName(self, name):
        if self.loaded == 0:
            self.read();
        for row in self.index:
            if row['name'] == name:
                return row['id'];
        return -1;
    # end def getIDFromName(self, name)

    def getNameFromID(self, id):
        if self.loaded == 0:
            self.read();
        if id > len(self.index):
            return "Not Found.";
        if id < 0:
            return "Not Found.";
        for row in self.index:
            if row['id'] == id:
                return row['name'];
    # end def getNameFromID(self, id)

    def addName(self, name):
        pos = len(self.index) + 1
        self.index.append({'id': pos, 'name': name});
        return pos;
    # end def addName(self, name)


# myIndex = CSVIndex()
