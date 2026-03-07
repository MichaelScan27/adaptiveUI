from enum import Enum

# Defines each state
class state(Enum): 
    CALM = "calm"
    NEUTRAL = "neutral"
    ENGAGED = "engaged"
    OVERLOADED = "overloaded"

# Rule-based transitions
TRANSITIONS = {
    state.CALM: [state.NEUTRAL],
    state.NEUTRAL: [state.CALM, state.ENGAGED],
    state.ENGAGED: [state.NEUTRAL, state.OVERLOADED],
    state.OVERLOADED: [state.ENGAGED]
}

## Hysteresis Thresholds
# CALM TO NEUTRAL
CALM_NEUTRAL_ENTER = 0.35
NEUTRAL_CALM_EXIT = 0.25

# NEUTRAL TO ENGAGED
NEUTRAL_ENGAGED_ENTER = 0.65
ENGAGED_NEUTRAL_EXIT = 0.55

# ENGAGED TO OVERLOADED
ENGAGED_OVERLOADED_ENTER = 0.85
OVERLOADED_ENGAGED_EXIT = 0.75

## Miscelaneous 
UPDATE_TIME = 0.2 # frequency of updates in seconds
DWELL_TIME = 1.5 # minimum dwell time in seconds
ALPHA = 0.25 # EMA Smoothing strength
