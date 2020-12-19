
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
        self.min_width = 0
        self.min_height = 0
        self.max_width = 0
        self.max_height = 0

        for i in range(len(newlist)):
            self.point_cloud.append(newlist[i])

        self.build_shape()

    def build_shape(self):
        total_widht = 0
        total_height = 0

        size_list = len(self.point_cloud)

        for i in range(size_list):
            total_widht += self.point_cloud[i][0]
            total_height += self.point_cloud[i][1]
            self.check_max_values(self.point_cloud[i][0], self.point_cloud[i][1])

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

    def import_points(self, new_list):
        for i in range(len(new_list)):
            self.point_cloud.append(new_list[i])
        self.reset_values()
        self.build_shape()

    def reset_values(self):
        self.top_left = [0, 0]
        self.top_right = [0, 0]
        self.bot_left = [0, 0]
        self.bot_right = [0, 0]
        self.center = [0, 0]
        self.width = 0
        self.height = 0
        self.min_width = 0
        self.min_height = 0
        self.max_width = 0
        self.max_height = 0