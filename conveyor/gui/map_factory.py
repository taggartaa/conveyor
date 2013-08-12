from gamemap import Map, Tile
from conveyor.event_manager.events import MapPreloadEvent, MapCreatedEvent, QuitEvent
from conveyor.event_manager import event_manager
from xml.dom import minidom
import os

class MapFactory(object):
    ''' Map Factory Class
        Manufacutres Map objects and sends them to the eventhandler
        to whoever is listening
    '''
    
    def __init__(self):
        ''' Constructor
            event_manager - The event manager to send the Map creation events to.
        '''
        event_manager.register_listener(self, [MapPreloadEvent, QuitEvent])

    def notify(self, event):
        ''' called whenever an event occurs that this class is listening too
            event - the event that occured.
        '''
        if isinstance(event, MapPreloadEvent):
            self._create_map(event.element)

        elif isinstance(event, QuitEvent):
            event_manager.unregister_listener(self)

    def _create_map(self, element):
        ''' private function that creates a Map
            element - an xml element defining how the Map is created.
        '''
        key = element.attributes['key'].value
        active = element.attributes['active'].value.lower() == 'true'
        tmp = element.attributes['size'].value.lower().split('x')
        size = (int(tmp[0]), int(tmp[1]))
        tmp = element.attributes['unit_size'].value.lower().split('x')
        unit_size = (int(tmp[0]), int(tmp[1]))
        
        tiles = []
        
        xmldoc = minidom.parse(element.attributes['map'].value)
        for tile in xmldoc.getElementsByTagName('tile'):
            sprite_key = tile.attributes['sprite'].value
            x = int(tile.attributes['x'].value)
            y = int(tile.attributes['y'].value)
            tiles.append(Tile(0, sprite_key, x, y))
                
        map = Map(key, 0, tiles, active, size, unit_size)
        event_manager.post(MapCreatedEvent(map))
            
 
