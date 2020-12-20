
class Temporary_shape:
    def __init__(self, new_entries):
        self.entries = new_entries
        self.new_entries = []
        self.point_list = []

    def import_new_list(self, new_list):
        for i in range(len(new_list)):
            self.point_list.append(new_list[i])
        test = 0

    def push_entries(self):
        for i in range(len(self.entries)):
            self.point_list.append(self.entries[i][0])
            self.point_list.append(self.entries[i][1])

        self.entries.clear()
        for i in range(len(self.new_entries)):
            self.entries.append(self.new_entries[i])
        self.new_entries.clear()
        test = 0

    def import_entries(self, list):
        for i in range(len(list)):
            self.new_entries.append(list[i])
        test = 0

    def close_entries(self):
        for i in range(len(self.entries)):
            self.point_list.append(self.entries[i][0])
            self.point_list.append(self.entries[i][1])