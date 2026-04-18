from flask import Flask, render_template, jsonify

import time
import threading
import json
from pathlib import Path
from state_system.state_system import StateSystem
from state_system.config import UPDATE_TIME
from state_system.FakeSignalGenerator import FakeSignalGenerator
from state_system.PresetSignal import PresetSignal
from state_system.config import SIGNAL_A
from state_system.config import SIGNAL_B
from state_system.config import SIGNAL_C


Path("logs").mkdir(exist_ok=True) # creates logs/ directory if it doesn't already exist
timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = Path(f"logs/log_{timestamp}.jsonl")

previousState = None
generator = None
signal = None

#region Methods 
def generator_system_init():
    global sm, generator, thread, state_loop_run, use_gen
    if (generator is not None):
        generator.stop()
    if (signal is not None):
        signal.stop()
    use_gen = True
    state_loop_run = True
    sm = StateSystem()
    generator = FakeSignalGenerator()
    generator.start()
    thread = threading.Thread(target=state_loop, daemon=True)
    thread.start()

def preset_system_init(preset):
    global sm, signal, thread, state_loop_run, use_gen
    if (generator is not None):
        generator.stop()
    if (signal is not None):
        signal.stop()
    use_gen = False
    state_loop_run = True
    sm = StateSystem()
    signal = PresetSignal(preset)
    signal.start()
    thread = threading.Thread(target=state_loop, daemon=True)
    thread.start()

def state_system_kill():
    global state_loop_run, thread, use_gen, signal, generator
    state_loop_run = False
    use_gen = False
    if (generator is not None):
        generator.stop()
    if (signal is not None):
        signal.stop()
    thread.join()

def state_loop():
    global previousState, use_gen
    while state_loop_run:
        if (use_gen):
            arousal = generator.get_value()
        else:
            arousal = signal.get_value()
        state = sm.update(arousal)
        if (previousState != None and previousState != state):
            response = {
                "time_sec": time.monotonic() - sm.init_time,
                "arousal": sm.smoothed_arousal,
                "state": sm.state.value,
                "stability": sm.stability,
                "state_duration": time.monotonic() - sm.state_start_time
            }
            with LOG_FILE.open("a") as f:
                f.write(json.dumps(response) + "\n")
        
        # print(
        #     "time_sec:       ", time.monotonic() - sm.init_time, "\n",
        #     "state_duration: ", time.monotonic() - sm.state_start_time, "\n",
        #     "arousal:        ", arousal, "\n",
        #     "state:          ", state, "\n",
        #     "stability:      ", sm.stability, "\n", 
        # )

        previousState = state
        time.sleep(UPDATE_TIME)

#endregion

#region FLASK
app = Flask(
    __name__,
    template_folder="../frontend", # HTML
    static_folder="../frontend/static" # CSS and JS
)

#region Routes
@app.route("/") # Serves the webpage
def home():
    return render_template("index.html")

@app.route("/api/state") # Returns the status of the state system
def get_state():
    response = {
        "time_sec": time.monotonic() - sm.init_time,
        "arousal": sm.smoothed_arousal,
        "state": sm.state.value,
        "stability": sm.stability,
        "state_duration": time.monotonic() - sm.state_start_time
    }
    return jsonify(response)

@app.route("/api/reset") # Stops and immediately reinitializes the state system
def reset():
    state_system_kill()
    generator_system_init()
    return {"status": "reset"}

@app.route("/api/kill") # Stops the state system
def kill():
    state_system_kill()
    return {"status": "kill"}

#region Init Processes

@app.route("/api/init_gen") # Starts the state system WITH fake signal generator
def start():
    generator_system_init()
    return {"status": "init_gen"}

@app.route("/api/init_a") # Starts the state system using a preset signal A
def startA():
    preset_system_init(SIGNAL_A)
    return {"status": "init_A"}

@app.route("/api/init_b") # Starts the state system using a preset signal B
def startB():
    preset_system_init(SIGNAL_B)
    return {"status": "init_B"}

@app.route("/api/init_c") # Starts the state system using a preset signal B
def startC():
    preset_system_init(SIGNAL_C)
    return {"status": "init_C"}


#endregion
#endregion

if __name__ == "__main__":
    # state_system_init()
    # high_low_high_init()
    app.run(debug=True, use_reloader=False)
#endregion