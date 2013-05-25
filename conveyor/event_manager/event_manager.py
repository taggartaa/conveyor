'''
Events and the event manager.
'''

from weakref import WeakKeyDictionary
import copy

from .events import Event

#------------------------------------------------------------------------------
class EventManager(object):
    ''' this object is responsible for coordinating most communication
        between the Model, View, and Controller.
    '''
    def __init__(self):
	self._listeners = dict()
	self._event_queue= []

    #----------------------------------------------------------------------
    def register_listener( self, listener, event_list):
        '''Registers a listener to be notified when events occur.
                listener   - The listener object that is being registerd.
                event_list - The list of events to listen for (These are classes, not instances).
        '''
        for eventType in event_list:
            if issubclass(eventType, Event):
                if self._listeners.has_key(eventType):
                    self._listeners[eventType][listener] = 1
                else:
                    self._listeners[eventType] = WeakKeyDictionary()
                    self._listeners[eventType][listener] = 1

    #----------------------------------------------------------------------
    def unregister_listener( self, listener, event_list=None ):
        ''' Removes the listener from listening for the specified events
                listener   - the listener object to be unregistered. 
                event_list - list of events to stop listening to.
                             if None, the listner is removed from all events.
        '''
        if event_list == None:
            for eventType in self._listeners.keys():
                if self._listeners[eventType].has_key(listener):
                    del self._listeners[eventType][listener]
        else:
            for eventType in event_list:
                if self._listeners.has_key(eventType):
                    if self._listeners[eventType].has_key(listener):
                        del self._listeners[eventType][listener]
		
    #----------------------------------------------------------------------
    def _fire( self, event ):
        ''' Notify all objects listening of the event that occured.
                event - The event that occured.
        '''
        eventType = type(event)
        if not issubclass(eventType, Event):
            return

        if self._listeners.has_key(eventType):
            for listener in self._listeners[eventType].keys():
                #NOTE: If the weakref has died, it will be 
                #automatically removed, so we don't have 
                #to worry about it.
                listener.notify(event)

        # Trickle events up the ladder
        for base in eventType.__bases__:
            if base != object:
                event_copy = copy.copy(event)
                event_copy.__class__ = base
                self._fire(event_copy)

    def fire_events( self ):
        ''' Notify all objects listening of events that have occured
        '''
        # note that the event_queue can grow while this loop is running,
        # so only process the events that were in there to begin with.
        event_queue_length = len(self._event_queue)
        for i in range(event_queue_length):
            self._fire(self._event_queue[0])
            self._event_queue.pop(0)
            

    def post( self, event ):
        ''' Add an event to the event queue.
            event - The event to be added to the queue
        '''
        self._event_queue.append(event)
#------------------------------------------------------------------------------
