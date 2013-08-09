from conveyor.common import enum
from conveyor.event_manager.events import GameStartedEvent, ResourcesLoadedEvent, QuitEvent
from conveyor.event_manager import event_manager
from conveyor.input import KeyboardController
from conveyor.gui import View
from conveyor.resource.config import ConfigurationController

from cpu_spinner import CPUSpinnerController

STATE = enum('Preparing', 'Running', 'Paused')

class Game(object):
    """..."""
    def __init__(self, data_path):
        event_manager.register_listener(self, [ResourcesLoadedEvent, QuitEvent])
        self._state = STATE.Preparing

        self._initialize_components(data_path)

    def _start(self):
        self._state = STATE.Running
        event_manager.post(GameStartedEvent(self))

    def notify(self, event):
        if isinstance(event, ResourcesLoadedEvent):
            if self._state == STATE.Preparing:
                self._start()

            elif isinstance(event, QuitEvent):
                    event_manager.unregister_listener(self)

    def _initialize_components(self, data_path):
        self._keyboard_controller = KeyboardController()
        self._cpu_spinner = CPUSpinnerController()
        self._configuration_controller = ConfigurationController(data_path)
        self._view = View()

    def start(self):
        self._cpu_spinner.run()
		
