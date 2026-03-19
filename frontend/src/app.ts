var duration;
var time_sec;
var state;
var arousal;
var stability;

setTheme('calm')
setInterval(checkState, 200);
const resetBtn = document.getElementById("resetBtn");
resetBtn?.addEventListener("click", async () => {
  const res = await fetch("/api/reset");
});

function setTheme(state : string ) {
  document.body.className = state;
}

async function checkState() {
  const res = await fetch("/api/state");
  const data = await res.json();
  setTheme(data.state);
  updateDashboard(data)

function updateDashboard(data: any) {
    duration = data.state_duration;
    time_sec = data.time_sec;
    state = data.state;
    arousal = data.arousal;
    stability = data.stability;
    const displayTimeSec = document.getElementById('system-duration');
    if (displayTimeSec) {
      const roundedTimeSec = Math.floor(time_sec * 100)/100;
      displayTimeSec.textContent = `TOTAL: ${roundedTimeSec} seconds`;
    }
    const displayDuration = document.getElementById('system-time_sec');
    if (displayDuration) {
      const roundedDuration = Math.floor(duration * 100)/100;
      displayDuration.textContent = `TIME_SEC: ${roundedDuration} seconds`;
    }
    const displayArousal = document.getElementById('system-arousal');
    if (displayArousal) {
      const roundedArousal = Math.floor(arousal * 100);
      displayArousal.textContent = `AROUSAL: ${roundedArousal}%`;
    }
    const displayState = document.getElementById('system-state');
    if (displayState) {
      displayState.textContent = `STATE: ${state}`;
    }
    const displayStability = document.getElementById('system-stability');
    if (displayStability) {
      const roundedStability = Math.floor(stability * 100);
      displayStability.textContent = `STABILITY: ${roundedStability}%`;
    }
  }
}
