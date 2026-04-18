import random
import time
import threading
from .config import UPDATE_TIME

class PresetSignal:
    def __init__(self, signalList, baseline=0.0 ):
        self.value = baseline
        self.signalList = signalList
        self.lock = threading.Lock()
        self.running = False
        self.index = 0

    def _loop(self): 
        while self.running: 
            if self.index >= len (self.signalList):
                self.index = 0

            self.value = self.signalList[self.index]
            self.index += 1 
            
            time.sleep(UPDATE_TIME) # Time-gap between each data point

    # Threading is necessary so the signal is continuous and does not only advance when the next value is needed.
    # Threads must be started and stopped--execution of loop code is also controlled by boolean
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()
    
    def get_value(self): 
        with self.lock: # Lock prevents accessing a bad/mid-write value since this is running concurrently with other processes
            return self.value