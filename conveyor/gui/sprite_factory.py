from .sprite import Sprite
from conveyor.event_manager.events import SpritePreloadEvent, SpriteCreatedEvent, QuitEvent
from conveyor.event_manager import event_manager
from conveyor.resource.resources import resources
from xml.dom import minidom
import os

class SpriteFactory(object):
    ''' Sprite Factory Class
        Manufacutres Sprite objects and sends them to the eventhandler
        to whoever is listening
    '''
    
    def __init__(self):
        ''' Constructor
            event_manager - The event manager to send the Sprite creation events to.
        '''
        event_manager.register_listener(self, [SpritePreloadEvent, QuitEvent])

    def notify(self, event):
        ''' called whenever an event occurs that this class is listening too
            event - the event that occured.
        '''
        if isinstance(event, SpritePreloadEvent):
            self._create_sprite(event.element)

        elif isinstance(event, QuitEvent):
            event_manager.unregister_listener(self)

    def _create_sprite(self, element):
        ''' private function that creates a Sprite
            properties - a dictionary of properties defining how the Sprite is created.
        '''
        key = element.attributes['key'].value
        sprite_sheet_key = element.attributes['spritesheet'].value
        rows = int(element.attributes['height'].value)
        columns = int(element.attributes['width'].value)
        width =  columns * resources[sprite_sheet_key].tile_width
        height = rows * resources[sprite_sheet_key].tile_height
        tile_map = self._get_tile_map(element, columns)
        
        sprite = Sprite(key, sprite_sheet_key, tile_map, width, height)
        event_manager.post(SpriteCreatedEvent(sprite))

    def _get_tile_map(self, element, columns):
        ''' Creates tile_map from an xml element '''
        tile_map = []
        count = 0
        for tile in element.getElementsByTagName('tile'):
            if int(count/columns) == len(tile_map):
                tile_map.append([])
            
            tile_map[count/columns].append(int(tile.attributes['gid'].value))
            count += 1
        
        return tile_map
