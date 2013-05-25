import numpy

class Vector(object):
    def __init__(self, x=0, y=0):
        self._vector = numpy.array([float(x),float(y)])
        
    @property
    def x(self):
        return self._vector[0]

    @x.setter
    def x(self, value):
        self._vector[0] = value

    @property
    def y(self):
        return self._vector[1]

    @y.setter
    def y(self, value):
        self._vector[1] = value

    @property
    def length(self):
        return numpy.linalg.norm(self._vector)

    def int(self):
        return Vector(int(self.x), int(self.y))

    def __str__(self):
        return "(%s, %s)"%(self.x, self.y)

    def __repr__(self):
        return str(self)

    def _to_vector(self, array):
        return Vector(array[0], array[1])

    def _get_value(self, other):
        if isinstance(other, Vector):
            return other._vector
        else:
            return other

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self._to_vector(self._vector.dot(other._vector))
        else:
            return self._to_vector(self._vector * other)

    def __add__(self, other):
        return self._to_vector(self._vector + self._get_value(other))

    def __sub__(self, other):
        return self._to_vector(self._vector - self._get_value(other))

    def __div__(self, other):
        return self._to_vector(self._vector/self._get_value(other))

    def __imul__(self, other):
        self._vector *= self._get_value(other)
        return self

    def __iadd__(self, other):
        self._vector += self._get_value(other)
        return self

    def __idiv__(self, other):
        self._vector /= self._get_value(other)
        return self

    def __isub__(self, other):
        self._vector -= self._get_value(other)
        return self
