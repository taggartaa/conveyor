from gamemap import Map
from conveyor.event_manager.events import MapPreloadEvent, MapCreatedEvent, QuitEvent
import os

class MapFactory(object):
    ''' Map Factory Class
        Manufacutres Map objects and sends them to the eventhandler
        to whoever is listening
    '''
    
    def __init__(self, event_manager):
        ''' Constructor
            event_manager - The event manager to send the Map creation events to.
        '''
        self._event_manager = event_manager
        self._event_manager.register_listener(self, [MapPreloadEvent, QuitEvent])

    def notify(self, event):
        ''' called whenever an event occurs that this class is listening too
            event - the event that occured.
        '''
        if isinstance(event, MapPreloadEvent):
            self._create_map(event.properties)

        elif isinstance(event, QuitEvent):
            self._event_manager.unregister_listener(self)

    def _create_map(self, properties):
        ''' private function that creates a Map
            properties - a dictionary of properties defining how the Map is created.
        '''
        key = properties['key']
        layer = int(properties['layer'])
        sprite_sheet_key = properties['sprite']
        tile_map = self._get_tile_map(properties['map'])
        char_definitions = self._get_char_definitions(properties['char_map'])
        active = (properties['active'].lower() == 'true')
        game_map = Map(key, self._event_manager, layer, sprite_sheet_key, tile_map, char_definitions, active)
        self._event_manager.post(MapCreatedEvent(game_map))

    def _get_tile_map(self, filename):
        ''' private function that reads tile placement from a file.
            filename - name of file that the tile_map is in.
        '''
        tile_map = []
        map_file = open(filename, 'r')
        for line in map_file:
            tile_map.append(line.strip('\n'))
        return tile_map

    def _get_char_definitions(self, def_string):
        ''' private function that builds a dictionary that maps characters to their sprite number.
            def_string - the string that must be parsed to build a dictionary e.g. /:0,_:1,\:2,|:3,L:6,7:8
        '''
        char_definitions = dict()
        for item in def_string.split(','):
            char,num = item.split(':')
            char_definitions[char] = int(num)
        return char_definitions
