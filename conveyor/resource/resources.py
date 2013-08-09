from conveyor.event_manager.events import FactoryObjectCreatedEvent, QuitEvent
from conveyor.event_manager import event_manager

class Resources(object):
    def __init__(self):
        event_manager.register_listener(self, [FactoryObjectCreatedEvent])
        self.resource_dictionary = dict()

    def notify(self, event):
        if isinstance(event, FactoryObjectCreatedEvent):
            if hasattr(event.obj, 'key'):
                self.resource_dictionary[event.obj.key] = event.obj
                
        elif isinstance(event, QuitEvent):
            event_manager.unregister_listener(self)
            
    def __getitem__(self, index):
        return self.resource_dictionary[index]
        
resources = Resources()