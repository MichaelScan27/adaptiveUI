import time

from state_system.state_system import StateSystem
from state_system.config import UPDATE_TIME

sm = StateSystem()

values = [
    0.1,
    0.2,
    0.4,
    0.6,
    0.8,
    0.95,
    0.95,
    0.95,
    0.95,
     0.95,
    0.95,
    0.95,
     0.95,
    0.95,
    0.95,
     0.95,
    0.95,
    0.95,
     0.95,
    0.95,
    0.95,
     0.95,
    0.95,
    0.95,
    0.93,
    0.93,
    0.93,
    0.3,
]

i = 1
for v in values:
    state = sm.update(v)
    
    print(
        "Update #", i, "\n"
        "time_sec: ", time.time() - sm.state_start_time, "\n",
        "arousal: ", v, "\n",
        "state: ", state, "\n",
        "stability: ", sm.stability, "\n", 
     )

    time.sleep(UPDATE_TIME)
    i+=1