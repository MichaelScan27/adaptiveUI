//#region Variables and timers
var duration;
var time_sec;
var state;
var arousal;
var stability;
let stateInterval : any = null;
//#endregion

//#region INIT
setTheme('calm')
stateInterval = setInterval(checkState, 200);
//#endregion

//#region Buttons
// Controls state machine
const resetBtn = document.getElementById("resetBtn");
resetBtn?.addEventListener("click", async () => {
  const res = await fetch("/api/reset");
});
const killBtn = document.getElementById("killBtn");
killBtn?.addEventListener("click", async () => {
  const res = await fetch("/api/kill");
  clearInterval(stateInterval);
  stateInterval = null;
});
const initBtn = document.getElementById("initBtn");
initBtn?.addEventListener("click", async () => {
  const res = await fetch("/api/init");
  stateInterval = setInterval(checkState, 200);
});

// Used when machine is paused to showcase each state
const calmBtn = document.getElementById("calmBtn");
calmBtn?.addEventListener("click", async () => {
  setTheme('calm')
});
const neutralBtn = document.getElementById("neutralBtn");
neutralBtn?.addEventListener("click", async () => {
  setTheme('neutral')
});
const engagedBtn = document.getElementById("engagedBtn");
engagedBtn?.addEventListener("click", async () => {
  setTheme('engaged')
});
const overloadedBtn = document.getElementById("overloadedBtn");
overloadedBtn?.addEventListener("click", async () => {
  setTheme('overloaded')
});
//#endregion 

//#region Theme Functions
function setTheme(state : string ) {
  document.body.className = state;
  const styles = getComputedStyle(document.body);
  const count = parseFloat(styles.getPropertyValue("--count")); // Gets --count value from /frontend/static/themes.css
  updateLayout(count);
  if (state == "overloaded"){
    explodeLayout();
  }
  if (state == "neutral") {
    shrinkLayout();
  }
}

function updateLayout(count: number) {
  const objects = document.querySelectorAll<HTMLElement>(".object"); 
  // Finds all objects, checks their i value against the given count, and displays accordingly.  Updates when we change theme.

  objects.forEach((el) => {
    const i = parseFloat(getComputedStyle(el).getPropertyValue("--i"));

    if (i < count) {
      const angle = (i * 360) / count;
      el.style.setProperty("--angle", `${angle}deg`);
      el.style.opacity = "1";
    } else {
      el.style.opacity = "0"; // Do not display element if it is not within count
    }
    
  });
}

function explodeLayout() {
  const objects = document.querySelectorAll<HTMLElement>(".object"); 

  objects.forEach((el) => {
    const i = parseFloat(getComputedStyle(el).getPropertyValue("--i"));

    if (i % 2 == 0) {
      el.style.scale = (Math.random() * 3).toString()
    }
  });
}

function shrinkLayout() {
  const objects = document.querySelectorAll<HTMLElement>(".object"); 

  objects.forEach((el) => {
    const i = parseFloat(getComputedStyle(el).getPropertyValue("--i"));

    if (i % 2 == 0) {
      el.style.scale = "1"
    }
  });
}

async function checkState() {
  const res = await fetch("/api/state");
  const data = await res.json();
  setTheme(data.state);
  updateDashboard(data)
}
//#endregion

//#region Info Functons
function updateDashboard(data: any) {
  // Match json values to variables
  duration = data.state_duration;
  time_sec = data.time_sec;
  state = data.state;
  arousal = data.arousal;
  stability = data.stability;

  // Get HTML element and set variable into template textContent.
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
//#endregion


