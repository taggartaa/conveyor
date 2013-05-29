from gamemap import Map
from conveyor.event_manager.events import MapPreloadEvent, MapCreatedEvent, QuitEvent
from xml.dom import minidom
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
            if event.properties['type'] == 'map':
                self._create_map(event.properties)
            elif event.properties['type'] in ['xml', 'tmx']:
                self._create_map_from_xml(event.properties)

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

    def _create_map_from_xml(self, properties):
        ''' Creates maps from an xml document '''
        count = 0
        key = properties['key']
        sprite_sheet_key = properties['sprite']
        active = properties['active'].lower() == 'true'

        xmldoc = minidom.parse(properties['map'])
        for layer in xmldoc.getElementsByTagName('layer'):
            layer_name = layer.getAttribute('name')
            tile_map, char_definitions = self._get_tile_map_xml(layer)
            game_map = Map('%s_%s'%(key, count), self._event_manager, layer_name, sprite_sheet_key, tile_map, char_definitions, active)
            self._event_manager.post(MapCreatedEvent(game_map))
            count += 1
            
        

    def _get_tile_map(self, filename):
        ''' private function that reads tile placement from a file.
            filename - name of file that the tile_map is in.
        '''
        tile_map = []
        map_file = open(filename, 'r')
        for line in map_file:
            tile_map.append(line.strip('\n'))
        return tile_map

    def _get_tile_map_xml(self, layer):
        tile_map = []
        char_definitions = dict()
        width = int(layer.getAttribute('width'))
        count = width
        for tile in layer.getElementsByTagName('tile'):
            if count == width:
                tile_map.append([])
                count = 0
            gid = int(tile.getAttribute('gid'))-1
            tile_map[-1].append(gid)
            if gid > 0 and not char_definitions.has_key(gid):
                char_definitions[gid] = gid
            count += 1
        return tile_map, char_definitions
        
        

    def _get_char_definitions(self, def_string):
        ''' private function that builds a dictionary that maps characters to their sprite number.
            def_string - the string that must be parsed to build a dictionary e.g. /:0,_:1,\:2,|:3,L:6,7:8
        '''
        char_definitions = dict()
        for item in def_string.split(','):
            char,num = item.split(':')
            char_definitions[char] = int(num)
        return char_definitions
