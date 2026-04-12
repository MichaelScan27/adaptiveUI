from flask import Flask, render_template, jsonify

import time
import threading
import json
from pathlib import Path
from state_system.state_system import StateSystem
from state_system.config import UPDATE_TIME
from state_system.FakeSignalGenerator import FakeSignalGenerator

Path("logs").mkdir(exist_ok=True) # creates logs/ directory if it doesn't already exist
timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = Path(f"logs/log_{timestamp}.jsonl")

previousState = None

def state_system_init():
    global sm, generator, thread, state_loop_run
    state_loop_run = True
    sm = StateSystem()
    generator = FakeSignalGenerator()
    generator.start()
    thread = threading.Thread(target=state_loop, daemon=True)
    thread.start()

def state_system_kill():
    global state_loop_run, thread
    state_loop_run = False
    thread.join()

def state_loop():
    global previousState
    while state_loop_run:
        arousal = generator.get_value()
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

app = Flask(
    __name__,
    template_folder="../frontend", # HTML
    static_folder="../frontend/static" # CSS and JS
)

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
    state_system_init()
    return {"status": "reset"}

@app.route("/api/kill") # Stops the state system
def kill():
    state_system_kill()
    return {"status": "kill"}

@app.route("/api/init") # Starts the state system from a stopped state
def start():
    state_system_init()
    return {"status": "init"}



if __name__ == "__main__":
    state_system_init()
    app.run(debug=True, use_reloader=False)