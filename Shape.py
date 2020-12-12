
class Shape:
    def __init__(self, newlist):
        self.top_left = [0, 0]
        self.top_right = [0, 0]
        self.bot_left = [0, 0]
        self.bot_right = [0, 0]
        self.center = [0, 0]
        self.point_cloud = newlist
        self.width = 0
        self.height = 0
        self.build_shape(newlist)
        self.isEmpty = False

    def build_shape(self, newlist):
        total_widht = 0
        total_height = 0

        min_width = 0
        min_height = 0
        max_width = 0
        max_height = 0

        size_list = len(newlist)

        if size_list == 0:
            self.isEmpty = True
            return

        for i in range(size_list):
            total_widht += newlist[i][0]
            total_height += newlist[i][1]

            if max_width < newlist[i][0]:
                max_width = newlist[i][0]
                if min_width == 0:
                    min_width = max_width
            if max_height < newlist[i][1]:
                max_height = newlist[i][1]
                if min_height == 0:
                    min_height = max_height
            if min_width > newlist[i][0]:
                min_width = newlist[i][0]
            if min_height > newlist[i][1]:
                min_height = newlist[i][1]

        self.top_left = [min_width, min_height]
        self.top_right = [max_width, min_height]
        self.bot_left = [min_width, max_height]
        self.bot_right = [max_width, max_height]
        self.center = [round(total_widht/size_list), round(total_height/size_list)]
        self.width = max_width - min_width
        self.height = max_height - min_height

    def is_in_range(self, point_to_check):
        if self.top_left[0] <= point_to_check[0] <= self.top_right[0] and self.bot_left[1] <= point_to_check[1] <= self.bot_right[1]:
            return True
        return False
