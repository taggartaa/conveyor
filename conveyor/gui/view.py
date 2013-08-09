from conveyor.event_manager.events import GameStartedEvent, TickEvent, DrawLayerEvent, FactoryObjectCreatedEvent, \
                                          RefreshScreenEvent, ScrollEvent, RegisterKeyboardEvent, StartScrollUpEvent, \
                                          StartScrollDownEvent, StartScrollLeftEvent, StartScrollRightEvent, \
                                          StopScrollUpEvent, StopScrollDownEvent, StopScrollLeftEvent, StopScrollRightEvent, \
                                          StartZoomInEvent, StartZoomOutEvent, ZoomEvent, QuitEvent
                                          
from conveyor.event_manager import event_manager
                          
from gui_common import Drawable
from conveyor.collision_detection.shapes import Rectangle
from conveyor.collision_detection import RectangleCollisionDetectorNoRotation as CollisionDetector
from conveyor.common import DIRECTION, ZOOM, MOUSESCROLLUP, MOUSESCROLLDOWN
from conveyor.math import Vector
import pygame
import pygame.locals
import pygame.transform
import copy

class View(object):
    def __init__(self):
        event_manager.register_listener(self, [GameStartedEvent, FactoryObjectCreatedEvent,
                                                     RefreshScreenEvent, ScrollEvent, ZoomEvent, QuitEvent])
        self._original_view_rectangle = Rectangle(0, 0, 500, 500)
        self._view_rectangle = Rectangle(0, 0, 500, 500)
        self._view_bounds = None
        self._setup_pygame()
        self._setup_keyboard_events()
        self._layers = []
        self._scroll_velocity = Vector(0,0)
        self._scroll_buffer = Vector(0,0)
        self._scale_factor = 1

    def _setup_keyboard_events(self):
        event_manager.post(RegisterKeyboardEvent(pygame.locals.KEYDOWN, pygame.locals.K_UP   , StartScrollUpEvent))
        event_manager.post(RegisterKeyboardEvent(pygame.locals.KEYDOWN, pygame.locals.K_DOWN , StartScrollDownEvent))
        event_manager.post(RegisterKeyboardEvent(pygame.locals.KEYDOWN, pygame.locals.K_LEFT , StartScrollLeftEvent))
        event_manager.post(RegisterKeyboardEvent(pygame.locals.KEYDOWN, pygame.locals.K_RIGHT, StartScrollRightEvent))
        
        event_manager.post(RegisterKeyboardEvent(pygame.locals.KEYUP, pygame.locals.K_UP   , StopScrollUpEvent))
        event_manager.post(RegisterKeyboardEvent(pygame.locals.KEYUP, pygame.locals.K_DOWN , StopScrollDownEvent))
        event_manager.post(RegisterKeyboardEvent(pygame.locals.KEYUP, pygame.locals.K_LEFT , StopScrollLeftEvent))
        event_manager.post(RegisterKeyboardEvent(pygame.locals.KEYUP, pygame.locals.K_RIGHT, StopScrollRightEvent))

        event_manager.post(RegisterKeyboardEvent(pygame.locals.MOUSEBUTTONDOWN, MOUSESCROLLUP,   StartZoomInEvent))
        event_manager.post(RegisterKeyboardEvent(pygame.locals.MOUSEBUTTONDOWN, MOUSESCROLLDOWN, StartZoomOutEvent))
        

    def notify(self, event):
        if isinstance(event, TickEvent):
            self._redraw(event.since_last)
            
        elif isinstance(event, RefreshScreenEvent):
            self._refresh(event.surface)
            
        elif isinstance(event, ScrollEvent):
            self._set_scroll(event.direction, event.speed)

        elif isinstance(event, ZoomEvent):
            self._set_zoom(event.direction, event.speed)
            
        elif isinstance(event, FactoryObjectCreatedEvent):
            if isinstance(event.obj, Drawable):
                if event.obj.layer not in self._layers:
                    self._layers.append(event.obj.layer)
                    #self._layers.sort()
                    
        elif isinstance(event, GameStartedEvent):
            event_manager.unregister_listener(self, [GameStartedEvent])
            event_manager.register_listener(self, [TickEvent])
            
        elif isinstance(event, QuitEvent):
            pygame.display.quit()
            event_manager.unregister_listener(self)
            
    def _setup_pygame(self):
        pygame.init()
        self._window = pygame.display.set_mode((self._view_rectangle.width, self._view_rectangle.height))
        pygame.display.set_caption('Conveyor')

    def _scale(self):
        tmp = self._original_view_rectangle.scaled(self._scale_factor)
        self._view_rectangle.width = tmp.width
        self._view_rectangle.height = tmp.height

    def _set_scroll(self, direction, speed):
        if direction == DIRECTION.Left:
            self._scroll_velocity.x -= speed
        elif direction == DIRECTION.Right:
            self._scroll_velocity.x += speed
        elif direction == DIRECTION.Up:
            self._scroll_velocity.y -= speed
        elif direction == DIRECTION.Down:
            self._scroll_velocity.y += speed

    def _set_zoom(self, direction, speed):
        if direction == ZOOM.In:
            self._scale_factor -= speed
        elif direction == ZOOM.Out:
            self._scale_factor += speed

        if self._scale_factor < 1:
            self._scale_factor = 1

    def _scroll(self, multiplier = 1):
        
        self._scroll_buffer += (self._scroll_velocity * multiplier)
        
        self._view_rectangle.x += int(self._scroll_buffer.x)
        self._view_rectangle.y += int(self._scroll_buffer.y)

        self._scroll_buffer -= self._scroll_buffer.int()
        
        self._check_bounds()
        
    def _check_bounds(self):
        if self._view_bounds == None:
            return True
        else:
            return False
            
        
    def _get_surface(self):
        surface = pygame.Surface((self._view_rectangle.width, self._view_rectangle.height), pygame.SRCALPHA, 32)
        surface.fill((255,255,255,255))
        return surface
        
    def _redraw(self, milseconds_passed):
        self._scroll(milseconds_passed/10.0)
        surface = self._get_surface()
        for layer in self._layers:
            event_manager.post(DrawLayerEvent(layer, surface, self._view_rectangle, self._scale_factor))

        event_manager.post(RefreshScreenEvent(surface))

    def _refresh(self, surface):
        self._window.blit(surface, (0,0))
        pygame.display.flip()
