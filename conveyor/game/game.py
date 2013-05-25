from conveyor.common import enum
from conveyor.event_manager.events import GameStartedEvent, ResourcesLoadedEvent, QuitEvent
from conveyor.event_manager import EventManager
from conveyor.input import KeyboardController
from conveyor.gui import View
from conveyor.resource import Resources, ConfigurationController

from cpu_spinner import CPUSpinnerController

STATE = enum('Preparing', 'Running', 'Paused')

class Game(object):
    """..."""
    def __init__(self, data_path):
        self._event_manager = EventManager()
        
	self._event_manager.register_listener(self, [ResourcesLoadedEvent, QuitEvent])
	self._state = STATE.Preparing

	self._initialize_components(data_path)

    def _start(self):
	self._state = STATE.Running
	self._event_manager.post(GameStartedEvent(self))

    def notify(self, event):
	if isinstance(event, ResourcesLoadedEvent):
	    if self._state == STATE.Preparing:
		self._start()

	    elif isinstance(event, QuitEvent):
                self._event_manager.unregister_listener(self)

    def _initialize_components(self, data_path):
        self._keyboard_controller = KeyboardController(self._event_manager)
        self._cpu_spinner = CPUSpinnerController(self._event_manager)
        self._configuration_controller = ConfigurationController(self._event_manager, data_path)
        self._view = View(self._event_manager)
        self._resources = Resources(self._event_manager)

    def start(self):
        self._cpu_spinner.run()
		
