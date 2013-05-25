from sprite import SpriteSheet
from conveyor.event_manager.events import SpriteSheetPreloadEvent, SpriteSheetCreatedEvent, QuitEvent

class SpriteSheetFactory(object):
    ''' SpriteSheet Factory Class
        Manufacutres SpriteSheet objects and sends them to the eventhandler
        to whoever is listening.
    '''
    def __init__(self, event_manager):
        ''' Constructor
            event_manager - the event manager to send SpriteSheet creation events to.
        '''
        self._event_manager = event_manager
        self._event_manager.register_listener(self, [SpriteSheetPreloadEvent, QuitEvent])


    def notify(self, event):
        ''' called whenever an event occurs that this class is listening too
            event - the event that occured.
        '''
        if isinstance(event, SpriteSheetPreloadEvent):
            self._create_sprite_sheet(event.properties)

        elif isinstance(event, QuitEvent):
            self._event_manager.unregister_listener(self)

    def _create_sprite_sheet(self, properties):
        ''' private function that creates a SpriteSheet
            properties - a dictionary of properties defining how the SpriteSheet is created.
        '''
        key = properties['key']
        filename = properties['image']
        tmp = properties['size'].lower().split('x')
        sheet_size = (int(tmp[0]), int(tmp[1]))
        tmp = properties['tile'].lower().split('x')
        tile_size = (int(tmp[0]), int(tmp[1]))
        sprite_sheet = SpriteSheet(key, filename, sheet_size, tile_size)
        self._event_manager.post(SpriteSheetCreatedEvent(sprite_sheet))
        
