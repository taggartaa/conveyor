import re
import os
from conveyor.event_manager.events import SpriteSheetPreloadEvent, SpritePreloadEvent, MapPreloadEvent, TickEvent, ResourcesLoadedEvent, QuitEvent
from conveyor.event_manager import event_manager
from conveyor.gui import MapFactory, SpriteSheetFactory, SpriteFactory
from xml.dom import minidom

class ConfigurationController(object):
    def __init__(self, data_path):
        event_manager.register_listener(self, [TickEvent, QuitEvent])
        self._map_factory = MapFactory()
        self._sprite_factory = SpriteFactory()
        self._sprite_sheet_factory = SpriteSheetFactory()
        self._load_step = 0
	
        self._load_order = ['spritesheet', 'sprite', 'map']
    
        self._tags = {'spritesheet' :   SpriteSheetPreloadEvent,
                      'sprite':         SpritePreloadEvent,
                      'map' :           MapPreloadEvent}

        self._paths = {'{DATA_PATH}' :      data_path,
                       '{IMAGES}' :         'images',
                       '{MAPS}' :           'maps'}

    def notify(self, event):
        if isinstance(event, TickEvent):
            try:
                if self._load_step == 0:
                    self._open_config_file()
                   
                self._load_current_step()   
                self._load_step += 1
                
                if self._load_step == len(self._load_order):
                    event_manager.unregister_listener(self, [TickEvent, QuitEvent])
                    self._close_config_file()
                    event_manager.post(ResourcesLoadedEvent())
            except:
                self._close_config_file()
                raise 
            
        elif isinstance(event, QuitEvent):
            event_manager.unregister_listener(self)
            
    def _open_config_file(self):
        try:
            config_file = open(os.path.join(self._paths['{DATA_PATH}'], 'config.xml'))
            self._xmldoc = minidom.parse(config_file)
            
        except:
            raise
            
        finally:
            config_file.close()
        
    def _close_config_file(self):
        pass
        #self._xmldoc.unlink()
        
    def _load_current_step(self):
        tag_name = self._load_order[self._load_step]
        for element in self._xmldoc.getElementsByTagName(tag_name):
            for attribute_key in element.attributes.keys():
                element.attributes[attribute_key].value = self._replace_paths(element.attributes[attribute_key].value)
                    
            EventType = self._tags[tag_name]
            event_manager.post(EventType(element))
            
    def _replace_paths(self, value):
        value_split = re.split('(%s)'%('|'.join(self._paths.keys())), value)
        for i in range(len(value_split)):
            if self._paths.has_key(value_split[i]):
                value_split[i] = self._paths[value_split[i]]
      
        if len(value_split) > 1:
            value = os.path.join(*value_split)
                    
        return value

