

class User:
    def __init__(self, name, height):
        self.name = name
        self.height = height

    def __repr__(self):
        return "{}".format(self.name)

    def save_user(self, name, height):
        pass
