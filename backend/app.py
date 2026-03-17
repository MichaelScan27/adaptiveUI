from flask import Flask, render_template, jsonify

import time
import threading
from state_system.state_system import StateSystem
from state_system.config import UPDATE_TIME
from state_system.FakeSignalGenerator import FakeSignalGenerator

sm = StateSystem()
generator = FakeSignalGenerator()
generator.start()

def state_loop():
    while True:

        arousal = generator.get_value()
        state = sm.update(arousal)
        
        # print(
        #     "Update #", i, "\n",
        #     "time_sec:       ", time.monotonic() - sm.init_time, "\n",
        #     "state_duration: ", time.monotonic() - sm.state_start_time, "\n",
        #     "arousal:        ", arousal, "\n",
        #     "state:          ", state, "\n",
        #     "stability:      ", sm.stability, "\n", 
        # )

        time.sleep(UPDATE_TIME)

threading.Thread(target=state_loop, daemon=True).start()


app = Flask(
    __name__,
    template_folder="../frontend",
    static_folder="../frontend/static"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/state")
def get_state():
    response = {
        "time_sec": time.monotonic() - sm.init_time,
        "arousal": sm.smoothed_arousal,
        "state": sm.state.value,
        "stability": sm.stability,
        "state_duration": time.monotonic() - sm.state_start_time
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
