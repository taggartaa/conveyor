from sprite import SpriteSheet
from conveyor.event_manager.events import SpriteSheetPreloadEvent, SpriteSheetCreatedEvent, QuitEvent
from conveyor.event_manager import event_manager

class SpriteSheetFactory(object):
    ''' SpriteSheet Factory Class
        Manufacutres SpriteSheet objects and sends them to the eventhandler
        to whoever is listening.
    '''
    def __init__(self):
        ''' Constructor
            event_manager - the event manager to send SpriteSheet creation events to.
        '''
        event_manager.register_listener(self, [SpriteSheetPreloadEvent, QuitEvent])


    def notify(self, event):
        ''' called whenever an event occurs that this class is listening too
            event - the event that occured.
        '''
        if isinstance(event, SpriteSheetPreloadEvent):
            self._create_sprite_sheet(event.element)

        elif isinstance(event, QuitEvent):
            event_manager.unregister_listener(self)

    def _create_sprite_sheet(self, element):
        ''' private function that creates a SpriteSheet
            element - an xml element with the attributes of the spritesheet
        '''
        key = element.attributes['key'].value
        filename = element.attributes['image'].value
        tmp = element.attributes['size'].value.lower().split('x')
        sheet_size = (int(tmp[0]), int(tmp[1]))
        tmp = element.attributes['tile'].value.lower().split('x')
        tile_size = (int(tmp[0]), int(tmp[1]))
        sprite_sheet = SpriteSheet(key, filename, sheet_size, tile_size)
        event_manager.post(SpriteSheetCreatedEvent(sprite_sheet))
        
