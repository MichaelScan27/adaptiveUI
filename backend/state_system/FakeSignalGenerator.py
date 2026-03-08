import random
import time
import threading
from .config import UPDATE_TIME

class FakeSignalGenerator:
    def __init__(self, baseline=0.0, drift=0.01, noise=0.3):
        self.value = baseline
        self.baseline = baseline
        self.drift = drift
        self.noise = noise
        self.lock = threading.Lock()
        self.running = False

    def _loop(self): 
        while self.running: 
            drift = random.gauss(0, self.drift) # Calculates an amount of drift to apply
            noise = random.gauss(0, self.noise) # Calculates an amount of noise to apply
            with self.lock: # Lock prevents self.value from being accessed mid-change
                self.value += drift + noise
                self.value += random.gauss(0, 0.01) # random noise
                self.value += random.uniform(-0.15, 0.15) # random spikes/depressions
                self.value = max(0.0, min(1.0, self.value)) # Clamp between 0.0 and 1.0
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