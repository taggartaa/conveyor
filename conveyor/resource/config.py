import re
import os
from conveyor.event_manager.events import SpriteSheetPreloadEvent, MapPreloadEvent, TickEvent, ResourcesLoadedEvent, QuitEvent
from conveyor.gui import MapFactory, SpriteSheetFactory
from xml.dom import minidom

class ConfigurationController(object):
    def __init__(self, event_manager, data_path):
        self._event_manager = event_manager
        self._event_manager.register_listener(self, [TickEvent, QuitEvent])
        self._map_factory = MapFactory(self._event_manager)
        self._sprite_sheet_factory = SpriteSheetFactory(self._event_manager)
	
        self._tags = {'sprite' :     SpriteSheetPreloadEvent,
                      'map' :        MapPreloadEvent}

        self._paths = {'{DATA_PATH}' :      data_path,
                       '{IMAGES}' :         'images',
                       '{MAPS}' :           'maps'}

    def notify(self, event):
        if isinstance(event, TickEvent):
            self._event_manager.unregister_listener(self, [TickEvent, QuitEvent])
            self._process_config_file()
            self._event_manager.post(ResourcesLoadedEvent())
            
        elif isinstance(event, QuitEvent):
            self._event_manager.unregister_listener(self)
            

    def _process_config_file(self):
        ''' Process the config file and fire off events to generate proper structures.
        '''
        config_file = open(os.path.join(self._paths['{DATA_PATH}'], 'config.xml'))

        try:
            xmldoc = minidom.parse(config_file)
	    
            for tag_name, EventType in self._tags.items():
                for element in xmldoc.getElementsByTagName(tag_name):
                    properties = dict()
                    for key, value in element.attributes.items():
                        properties[key] = self._replace_paths(value)
                    self._event_manager.post(EventType(properties))
        except:
            raise
        finally:
            config_file.close()
            
    def _replace_paths(self, value):
        value_split = re.split('(%s)'%('|'.join(self._paths.keys())), value)
        for i in range(len(value_split)):
            if self._paths.has_key(value_split[i]):
                value_split[i] = self._paths[value_split[i]]
      
        if len(value_split) > 1:
            value = os.path.join(*value_split)
                    
        return value

