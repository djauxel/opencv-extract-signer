class Frame:
    def __init__(self, topLeft = None, topRight = None, bottomRight = None, bottomLeft = None):
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomRight = bottomRight
        self.bottomLeft = bottomLeft

    @property
    def topLeft(self):
        return self.__topLeft
    
    @property
    def topRight(self):
        return self.__topRight
    
    @property
    def bottomRight(self):
        return self.__bottomRight

    @property
    def bottomLeft(self):
        return self.__bottomLeft

    @topLeft.setter
    def topLeft(self, value):
        self.__topLeft = value

    @topRight.setter
    def topRight(self, value):
        self.__topRight = value

    @bottomRight.setter
    def bottomRight(self, value):
        self.__bottomRight = value

    @bottomLeft.setter
    def bottomLeft(self, value):
        self.__bottomLeft = value