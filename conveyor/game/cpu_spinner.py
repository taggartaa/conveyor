from conveyor.event_manager.events import QuitEvent, TickEvent, RegisterKeyboardEvent
import pygame.locals
import pygame.time

class CPUSpinnerController(object):
    """..."""
    def __init__(self, event_manager):
	self.event_manager = event_manager
	self.event_manager.register_listener( self, [QuitEvent] )
	self.event_manager.post(RegisterKeyboardEvent(pygame.locals.KEYDOWN, pygame.locals.K_ESCAPE, QuitEvent))

	self.keep_going = True

    def run(self):
        last_tick = pygame.time.get_ticks()
	while self.keep_going:
            cur_tick = pygame.time.get_ticks()
	    self.event_manager.post( TickEvent(cur_tick - last_tick) )
	    self.event_manager.fire_events()
	    last_tick = cur_tick

    def notify(self, event):
	if isinstance( event, QuitEvent ):
	    #this will stop the while loop from running
	    self.keep_going = False
