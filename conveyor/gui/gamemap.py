from conveyor.event_manager.events import DrawLayerEvent, SpriteSheetCreatedEvent, QuitEvent
from gui_common import Drawable, Rectangle
import pygame

class Map(Drawable):
    ''' Used to draw a map to a surface on a particuler layer.
    '''
    def __init__(self, key, event_manager, layer, sprite_sheet_key, tile_map, char_definitions, active):
        ''' Constructor
            key             - A unique name given to this map.
            event_manager   - The event manager to post/get events from.
            layer           - The layer this Map is on.
            sprite_sheet    - The sprite sheet containing the tiles.
            tile_map        - The map indicating where to place tiles.
            char_definitinos- The map indicating which char represents which tile.
            active          - Determins if the map is currently visable.
        '''
        Drawable.__init__(self, layer)
        
        self.key = key
        self.sheet = None
        
        self._event_manager = event_manager
        self._event_manager.register_listener(self, [DrawLayerEvent, SpriteSheetCreatedEvent, QuitEvent])
        self._sprite_sheet_key = sprite_sheet_key
        self._sprite_sheet = None
        self._char_definitions = char_definitions
        self._tile_map = tile_map
        self._active = active

    def notify(self, event):
        ''' called whenever an event occurs that this class is listening too
            event - the event that occured.
        '''
        if isinstance(event, DrawLayerEvent) and event.layer == self._layer and self._active:
            self._draw(event.surface, event.rectangle, event.scale_factor)
            
        elif isinstance(event, SpriteSheetCreatedEvent) and event.obj.key == self._sprite_sheet_key:
            self._sprite_sheet = event.obj
            self.size = ((len(self._tile_map[0])*self._sprite_sheet.tile_width,
                          len(self._tile_map)*self._sprite_sheet.tile_height))
            self._cache_surface()
            
        elif isinstance(event, QuitEvent):
            self._event_manager.unregister_listener(self)
            
    def set_active(self, active=True):
        ''' Determines wheter or not this map is visable.
            active - If True, the map is currently visable.
        '''
        self._active = active

    def _cache_surface(self):
        self.original_image.fill((0,0,0,0))

        row_idx = 0
        char_idx = 0
        for row in self._tile_map:
            for char in row:
                if self._char_definitions.has_key(char):
                    self.original_image.blit(self._sprite_sheet[self._char_definitions[char]],
                                             (char_idx*self._sprite_sheet.tile_width,
                                              row_idx*self._sprite_sheet.tile_height))
                char_idx += 1
                    
            row_idx += 1
            char_idx = 0

        self.update_cache()

    def _draw(self, surface, rectangle, scale_factor):
        ''' Draws the map to the surface.
            surface - surface to draw the map on.
            rectangle - The portion of the layer that is visable
        '''
        self.scale(scale_factor)
        
        intersection = self.rect.intersection(rectangle)
        
        if intersection == None:
            return
        else:
            surface.blit(self.image.subsurface(intersection), (intersection.x - rectangle.x, intersection.y - rectangle.y))

        

        
