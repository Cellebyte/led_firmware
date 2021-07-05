class RGB:
    MIN = 0
    MAX = 255

    def __init__(self, r, g, b):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)

    def normalize(self):
        self.r = round(self.r)
        self.g = round(self.g)
        self.b = round(self.b)
        if self.r < self.MIN:
            self.r = self.MIN
        if self.g < self.MIN:
            self.g = self.MIN
        if self.b < self.MIN:
            self.b = self.MIN
        if self.r > self.MAX:
            self.r = self.MAX
        if self.g > self.MAX:
            self.g = self.MAX
        if self.b > self.MAX:
            self.b = self.MAX
        return self

    def as_dict(self):
        return {"r": self.r, "g": self.g, "b": self.b}

    def as_vector(self):
        return (self.r, self.g, self.b)

    def from_vector(self, vector):
        self.r = vector[0]
        self.g = vector[1]
        self.b = vector[2]

    def __add__(self, other):
        if isinstance(other, RGB):
            return RGB(self.r + other.r, self.g + other.g, self.b + other.b)
        else:
            raise ValueError("RGB is required")

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, RGB):
            return RGB(self.r - other.r, self.g - other.g, self.b - other.b)
        else:
            raise ValueError("RGB is required")

    def __rsub__(self, other):
        if isinstance(other, RGB):
            return RGB(other.r - self.r, other.g - self.g, other.b - self.b)
        else:
            raise ValueError("RGB is required")

    def __mul__(self, other):
        if isinstance(other, RGB):
            return RGB(self.r * other.r, self.g * other.g, self.b * other.b)
        else:
            raise ValueError("RGB is required")

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, int):
            return RGB(self.r / other, self.g / other, self.b / other)
        else:
            raise ValueError("Scalar <int> is required")

    def __repr__(self):
        return "RGB({},{},{})".format(self.r, self.g, self.b)
