from conveyor.event_manager.events import DrawLayerEvent, SpriteSheetCreatedEvent, QuitEvent
from conveyor.event_manager import event_manager
from gui_common import Drawable
from conveyor.collision_detection import RectangleCollisionDetectorNoRotation as CollisionDetector
from conveyor.collision_detection.shapes import Rectangle
import pygame

from conveyor.resource.resources import resources

class Tile(Drawable):
    def __init__(self, layer, sprite_key, x=0, y=0):
        Drawable.__init__(self, layer, x, y)
        self._sprite_key = sprite_key

    @property
    def size(self):
        return (resources[self._sprite_key].width, resources[self._sprite_key].height)

    @property
    def image(self):
        return resources[self._sprite_key].image

    @property
    def scale_factor(self):
        return resources[self._sprite_key].scale_factor
        
class Map(Drawable):
    ''' Used to draw a map to a surface on a particuler layer.
    '''
    def __init__(self, key, layer, tile_map, active, size, unit_size):
        ''' Constructor
            key             - A unique name given to this map.
            layer           - The layer this Map is on.
            tile_map        - The map indicating where to place tiles.
            active          - Determins if the map is currently visable.
            size            - The size of the map in pixels.
        '''
        Drawable.__init__(self, layer)
        
        self.key = key
        self.size = size
        
        event_manager.register_listener(self, [DrawLayerEvent, QuitEvent])
        self._tile_map = tile_map
        self._unit_size = unit_size
        self._active = active
        self._scale_factor = 1
        
        self.initialize()
        
    @property
    def size(self):
        return self._size
        
    @size.setter
    def size(self, value):
        self._size = value
        return value
        
    @property
    def image(self):
        return self._image
        
    @image.setter
    def image(self, value):
        self._image = value
        return value

    def initialize(self):
        self._cache = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        self._cache_rect = self.rect.copy()
        self._cache_surface()
        self.image = self._cache.copy()
    
    def notify(self, event):
        ''' called whenever an event occurs that this class is listening too
            event - the event that occured.
        '''
        if isinstance(event, DrawLayerEvent) and event.layer == self._layer and self._active:
            self._draw(event.surface, event.rectangle, event.scale_factor)
            
        elif isinstance(event, QuitEvent):
            event_manager.unregister_listener(self)
            
    def set_active(self, active=True):
        ''' Determines wheter or not this map is visable.
            active - If True, the map is currently visable.
        '''
        self._active = active
        
    def scale(self, scale_factor):
        if self._scale_factor != scale_factor:
            self._scale(scale_factor)
            
    def _scale(self, scale_factor):
        self.size = self._cache_rect.scaled(1.0/scale_factor).size
        self._scale_factor = scale_factor
        self.image = pygame.transform.smoothscale(self._cache, self.size)

    def _cache_surface(self):
        self._cache.fill((0,0,0,0))

        row_idx = 0
        col_idx = 0
        
        for row in self._tile_map:
            for sprite_key in row:
                if sprite_key != '':
                    print "Draw sprite on cache: %s (%d, %d)" %(sprite_key, col_idx*self._unit_size[0], row_idx*self._unit_size[1])
                    print "Affected area: %s" %(str(self._cache.blit(resources[sprite_key].image,(col_idx*self._unit_size[0], row_idx*self._unit_size[1])).size))
                    
                col_idx += 1
                    
            row_idx += 1
            col_idx = 0

    def _draw(self, surface, rectangle, scale_factor):
        ''' Draws the map to the surface.
            surface - surface to draw the map on.
            rectangle - The portion of the layer that is visable
        '''
        self.scale(scale_factor)
        
        intersection = CollisionDetector.intersection(self.rect, rectangle)
        
        if intersection == None:
            return
        else:
            surface.blit(self.image.subsurface(intersection), (intersection.x - rectangle.x, intersection.y - rectangle.y))

        

        
