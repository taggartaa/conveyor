from conveyor.event_manager.events import FactoryObjectCreatedEvent, QuitEvent

class Resources(object):
    def __init__(self, event_manager):
        self._event_manager = event_manager
        self._event_manager.register_listener(self, [FactoryObjectCreatedEvent])
        self.resource_dictionary = dict()

    def notify(self, event):
        if isinstance(event, FactoryObjectCreatedEvent):
            if hasattr(event.obj, 'key'):
                self.resource_dictionary[event.obj.key] = event.obj
                
        elif isinstance(event, QuitEvent):
            self._event_manager.unregister_listener(self)
