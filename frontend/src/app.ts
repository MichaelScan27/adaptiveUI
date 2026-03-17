var duration;
var state_dur;
var state;
var arousal;
var stability;

setTheme('calm')
const btn1 = document.getElementById("btn1");
const btn2 = document.getElementById("btn2");
const btn3 = document.getElementById("btn3");
const btn4 = document.getElementById("btn4");
const btn5 = document.getElementById("btn5");
btn1?.addEventListener("click", async () => {
  // const res = await fetch("/api/test");
  // const data = await res.json();
  setTheme('calm');
});
btn2?.addEventListener("click", async () => {
  setTheme('neutral');
});
btn3?.addEventListener("click", async () => {
  setTheme('engaged');
});
btn4?.addEventListener("click", async () => {
  setTheme('overloaded');
});
btn5?.addEventListener("click", async () => {
  const res = await fetch("/api/state");
  const data = await res.json();
  setTheme(data.state);
})


setInterval(checkState, 200);

function setTheme(state : string ) {
  document.body.className = state;
}

async function checkState() {
  const res = await fetch("/api/state");
  const data = await res.json();
  setTheme(data.state);
  state_dur = data.state_duration;
  duration = data.time_sec;
  state = data.state;
  arousal = data.arousal;
  stability = data.stability;


  const displayTotal = document.getElementById('system-total');
  if (displayTotal) {
    displayTotal.textContent = `TOTAL: ${duration}`;
  }
  const displayTime = document.getElementById('system-time_sec');
  if (displayTime) {
    displayTime.textContent = `STATE DURATION: ${state_dur}`;
  }
  const displayArousal = document.getElementById('system-arousal');
  if (displayArousal) {
    displayArousal.textContent = `AROUSAL: ${arousal}`;
  }
  const displayState = document.getElementById('system-state');
  if (displayState) {
    displayState.textContent = `STATE: ${state}`;
  }
  const displayStability = document.getElementById('system-stability');
  if (displayStability) {
    displayStability.textContent = `STABILITY: ${stability}`;
  }
}
