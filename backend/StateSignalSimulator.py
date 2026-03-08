import time

from state_system.state_system import StateSystem
from state_system.config import UPDATE_TIME
from state_system.FakeSignalGenerator import FakeSignalGenerator

sm = StateSystem()
generator = FakeSignalGenerator()
generator.start()

for i in range(200): # Run for 200 steps * UPDATE_TIME
    arousal = generator.get_value()
    state = sm.update(arousal)
    
    # Future data for JSON
    print(
        "Update #", i, "\n",
        "time_sec:       ", time.monotonic() - sm.init_time, "\n",
        "state_duration: ", time.monotonic() - sm.state_start_time, "\n",
        "arousal:        ", arousal, "\n",
        "state:          ", state, "\n",
        "stability:      ", sm.stability, "\n", 
    )

    time.sleep(UPDATE_TIME)

generator.stop()