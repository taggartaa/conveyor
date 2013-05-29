import pygame
from pygame.sprite import Sprite

class Rectangle(pygame.Rect):
    def __init__(self, x, y, width, height):
        pygame.Rect.__init__(self, x, y, width, height)

    def intersection(self, other):
        right_most_left_side = max(self.left, other.left)
        left_most_right_side = min(self.right, other.right)
        bottom_most_top_side = max(self.top, other.top)
        top_most_bottom_side = min(self.bottom, other.bottom)

        # If the left most ride side is left of the right most left side, no intersection
        if left_most_right_side <= right_most_left_side:
            return None
        # If the bottom most top side is below the top most bottom side, no intersection
        elif bottom_most_top_side >= top_most_bottom_side:
            return None
        else:
            return Rectangle(x = right_most_left_side,
                             y = bottom_most_top_side,
                             width = left_most_right_side - right_most_left_side,
                             height = top_most_bottom_side - bottom_most_top_side)

    def scaled(self, factor):
        return Rectangle(self.x, self.y, self.width*factor, self.height*factor)

    def __str__(self):
        return "(%s, %s) w: %s h:%s"%(self.x, self.y, self.width, self.height)

    def __repr__(self):
        return str(self)


class Drawable(Sprite):
    def __init__(self, layer, x = 0, y = 0, width = 0, height = 0):
        Sprite.__init__(self)

        self._original_rect = Rectangle(x, y, width, height)
        self.original_image = pygame.Surface((width, height), pygame.SRCALPHA, 32)

        self.rect = Rectangle(x, y, width, height)
        self.image = self.original_image.copy()
        
        self.layer = layer
        self.scale_factor = 1.0

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, value):
        self._layer = value

    @property
    def position(self):
        return self.rec.topleft

    @property
    def size(self):
        return self.rect.size

    @size.setter
    def size(self, value):
        self.rect.size = self._original_rect.size = value
        
        tmp = self.original_image
        self.original_image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.original_image.blit(tmp, (0,0))
        self.update_cache()

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = value

    @property
    def original_image(self):
        return self._original_image
    
    @original_image.setter
    def original_image(self, value):
        self._original_image = value

    @property
    def scale_factor(self):
        return self._scale_factor

    @scale_factor.setter
    def scale_factor(self, value):
        if value >= 1.0:
            self._scale_factor = float(value)

    def scale(self, scale_factor):
        if self._scale_factor != scale_factor and scale_factor != 0:
            self._scale(scale_factor)

    def _scale(self, factor):
        self.rect = self._original_rect.scaled(1.0/factor)
        self.image = pygame.transform.smoothscale(self.original_image, self.rect.size)
        self.scale_factor = factor

    def update_cache(self):
        self.image = self.original_image.copy()
        tmp = self.scale_factor
        self.scale_factor = 1.0
        self.scale(tmp)
