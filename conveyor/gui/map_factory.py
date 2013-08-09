from gamemap import Map
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
        
        tile_map = []
        
        xmldoc = minidom.parse(element.attributes['map'].value)
        for row in xmldoc.getElementsByTagName('row'):
            tile_map.append([])
            for tile in row.getElementsByTagName('tile'):
                tile_map[-1].append(tile.getAttribute('sprite'))
                
        map = Map(key, 0, tile_map, active, size, unit_size)
        event_manager.post(MapCreatedEvent(map))
            
 
