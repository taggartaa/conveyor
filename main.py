import os
import module_locator

from conveyor.game import Game
from conveyor.event_manager.events import *
from conveyor.event_manager import event_manager

class Debugger(object):
    def __init__(self):
        event_manager.register_listener(self, [Event])

    def notify(self, event):
        i = raw_input("Event: %s"%(event))
        if i != '':
            event_manager.unregister_listener(self)

class FpsViewer(object):
    def __init__(self):
        event_manager.register_listener(self, [TickEvent, RefreshScreenEvent])
        self._cur_time = 0
        self._refreshes = 0

    def notify(self, event):
        if isinstance(event, TickEvent):
            self._cur_time += event.since_last
            if self._cur_time >= 1000:
                print(self._refreshes)
                self._refreshes = 0
                self._cur_time -= 1000

        elif isinstance(event, RefreshScreenEvent):
            self._refreshes += 1

if __name__ == '__main__':
    data_path = os.path.join(module_locator.module_path(), "data")
    game = Game(data_path)
    #fps_viewer = FpsViewer()
    #debugger = Debugger()

    game.start()
