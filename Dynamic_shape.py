
class Dynamic_shape:
    def __init__(self):
        self.top_left = [0, 0]
        self.bot_right = [0, 0]
        self.center = [0, 0]
        self.width = 0
        self.height = 0

    def build(self, top, right, bot, left):
        self.top_left = [left, top]
        self.bot_right = [right, bot]
        self.width = right-left
        self.height = bot-top
        self.center = [left + (self.width/2), top + (self.height/2)]
