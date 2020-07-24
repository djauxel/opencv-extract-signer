class BoundingBox(object):
    def __init__(self, min_x = None, min_y = None, max_x = None, max_y = None):
        self.__min_x = min_x
        self.__min_y = min_y
        self.__max_x = max_x
        self.__max_y = max_y

    @property
    def min_x(self):
        return self.__min_x

    @property
    def min_y(self):
        return self.__min_y

    @property
    def max_x(self):
        return self.__max_x

    @property
    def max_y(self):
        return self.__max_y

    @min_x.setter
    def min_x(self, value):
        self.__min_x = value

    @min_y.setter
    def min_y(self, value):
        self.__min_y = value
    
    @max_x.setter
    def max_x(self, value):
        self.__max_x = value

    @max_y.setter
    def max_y(self, value):
        self.__max_y = value