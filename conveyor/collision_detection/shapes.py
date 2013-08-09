import pygame

class Rectangle(pygame.Rect):
    def __init__(self, x, y, width, height):
        pygame.Rect.__init__(self, x, y, width, height)

    def scaled(self, factor):
        return Rectangle(self.x, self.y, self.width*factor, self.height*factor)
        
    def copy(self):
        return Rectangle(self.x, self.y, self.width, self.height)

    def __str__(self):
        return "(%s, %s) w: %s h:%s"%(self.x, self.y, self.width, self.height)

    def __repr__(self):
        return str(self)