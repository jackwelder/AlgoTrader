class Stock:
    def __init__(self, name):
        self.name = name
        self.value = 0

    def __str__(self):
        return str(self.name + " Score is " + str(self.value))

