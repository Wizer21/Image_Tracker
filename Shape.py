
class Shape:
    def __init__(self, newlist):
        self.top_left = [0, 0]
        self.top_right = [0, 0]
        self.bot_left = [0, 0]
        self.bot_right = [0, 0]
        self.center = [0, 0]
        self.point_cloud = []
        self.width = 0
        self.height = 0
        self.isEmpty = False
        self.min_width = 0
        self.min_height = 0
        self.max_width = 0
        self.max_height = 0
        self.build_shape(newlist)

    def build_shape(self, newlist):
        total_widht = 0
        total_height = 0

        size_list = len(newlist)

        for i in range(size_list):
            total_widht += newlist[i][0][0]
            total_height += newlist[i][0][1]
            self.check_max_values(newlist[i][0][0], newlist[i][0][1])
            self.point_cloud.append(newlist[i][0])
            total_widht += newlist[i][1][0]
            total_height += newlist[i][1][1]
            self.check_max_values(newlist[i][1][0], newlist[i][1][1])
            self.point_cloud.append(newlist[i][1])

        self.top_left = [self.min_width, self.min_height]
        self.top_right = [self.max_width, self.min_height]
        self.bot_left = [self.min_width, self.max_height]
        self.bot_right = [self.max_width, self.max_height]
        self.center = [round(total_widht/size_list), round(total_height/size_list)]
        self.width = self.max_width - self.min_width
        self.height = self.max_height - self.min_height

    def is_in_range(self, point_to_check):
        in_width = self.top_left[0] <= point_to_check[0] <= self.bot_right[0]
        in_height = self.top_left[1] <= point_to_check[1] <= self.bot_right[1]
        if in_width and in_height:
            return True
        return False

    def check_max_values(self, new_widht, new_height):
        if self.max_width < new_widht:
            self.max_width = new_widht
            if self.min_width == 0:
                self.min_width = self.max_width
        if self.max_height < new_height:
            self.max_height = new_height
            if self.min_height == 0:
                self.min_height = self.max_height
        if self.min_width > new_widht:
            self.min_width = new_widht
        if self.min_height > new_height:
            self.min_height = new_height