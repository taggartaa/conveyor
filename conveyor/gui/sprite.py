import pygame
import os

from conveyor.collision_detection.shapes import Rectangle
from conveyor.event_manager import event_manager
from conveyor.resource.resources import resources

class Sprite(object):
    ''' Used to combine several pieces of a sprite sheet into one image.
    '''
    def __init__(self, key, sprite_sheet_key, tile_map, height, width):
        self.key = key
        self._sprite_sheet_key = sprite_sheet_key
        self._tile_map = tile_map
        self.height = height
        self.width = width
        
        self.initialize()
        
    @property
    def image(self):
        return self._original_image
        
    @image.setter
    def image(self, value):
        self._original_image = value
        return self._original_image
        
    def initialize(self):
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        
        for row in range(len(self._tile_map)):
            for column in range(len(self._tile_map[row])):
                if self._tile_map[row][column] > 0:
                    sprite_sheet = resources[self._sprite_sheet_key]
                    self.image.blit(sprite_sheet[self._tile_map[row][column]],
                                             (column*sprite_sheet.tile_width,
                                              row*sprite_sheet.tile_height))
        

class SpriteSheet(object):
    ''' Used to load a set of sprites from a sprite sheet.
    '''
    def __init__(self, key, filename, sheet_size, tile_size):
        self.key = key
        self.width, self.height = sheet_size
        self.tile_width, self.tile_height = tile_size
        self.filename = filename
        self._sheet = pygame.image.load(self.filename).convert_alpha()
        self._load_images()


    def _load_images(self):
        ''' Loads sprites into a list from left to right then top to bottom.'''
        tiles_across = int(self.width / self.tile_width)
        tiles_down = int(self.height / self.tile_height)
        rects = []
        for y in range(tiles_down):
            for x in range(tiles_across):
                rects.append(Rectangle(x*self.tile_width, y*self.tile_height, self.tile_width, self.tile_height))
                
        self._sprites = self._images_at(rects)
    
    def _image_at(self, rectangle):
        '''Loads image from x,y,x+offset,y+offset'''
        return self._sheet.subsurface(rectangle)
    
    def _images_at(self, rects):
        '''Loads multiple images, supply a list of coordinates''' 
        return [self._image_at(rect) for rect in rects]

    def __getitem__(self, index):
        return self._sprites[index]
