import pygame
from .sprite import Sprite
from conveyor.collision_detection.shapes import Rectangle
from abc import ABCMeta, abstractproperty

class Drawable(object):
    __metaclass__ = ABCMeta
    
    def __init__(self, layer, x=0, y=0):
    
        self.layer = layer
        self.x = x
        self.y = y

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, value):
        self._layer = value

    @property
    def position(self):
        return (self.x, self.y)
        
    @position.setter
    def position(self, value):
        self.x = value[0]
        self.y = value[1]
        return value

    @property
    def width(self):
        return self.size[0]
        
    @property
    def height(self):
        return self.size[1]
        
    @property
    def rect(self):
        return Rectangle(self.x, self.y, self.width, self.height)
        
    @abstractproperty
    def size(self):
        pass
        
    @abstractproperty
    def image(self):
        pass

