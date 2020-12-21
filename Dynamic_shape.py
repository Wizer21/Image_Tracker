
class Dynamic_shape:
    def __init__(self, top, right, bot, left):
        self.top_left = [0, 0]
        self.bot_right = [0, 0]
        self.center = [0, 0]
        self.width = 0
        self.height = 0

        self.build(top, right, bot, left)

    def build(self, top, right, bot, left):
        self.top_left = [top, left]
        self.bot_right = [bot, right]
        self.width = right-left
        self.height = bot-top
        self.center = [left + (self.width/2), bot + (self.height/2)]
