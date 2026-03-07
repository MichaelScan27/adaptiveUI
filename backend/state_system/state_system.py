import time
from .config import *

class StateSystem:
    def __init__(self): # Initializes system to a CALM state 
        self.state = state.CALM
        self.state_start_time = time.time()
        self.smoothed_arousal = 0.0
        self.stability = 0.0
        self.initialized = False

    # Main state update function that applies EMA, Dwell Time, and Hysteresis-based transitions
    def update(self, raw_arousal: float):
        # Applies Temporal Smoothing (EMA)
        if not self.initialized: 
            self.smoothed_arousal = raw_arousal # a-hat = a(0)
            self.initialized = True
        else:
            previous_smoothed_arousal = self.smoothed_arousal
            self.smoothed_arousal = ( # a-hat = 
                ALPHA * raw_arousal + (1 - ALPHA) * self.smoothed_arousal # alpha * a(t) + (1 - alpha) * a-hat
            )
            arousal_delta = self.smoothed_arousal - previous_smoothed_arousal
            self.stability = 1 / (1 + abs(arousal_delta))

        # Applies Minimum Dwell Time
        state_duration = time.time() - self.state_start_time 
        if (state_duration < DWELL_TIME):
            return self.state
        else:
            new_state = self.transition(self.smoothed_arousal)

        # Enforces rule-based state-transition logic 
        if (new_state != self.state) and (new_state in TRANSITIONS[self.state]): 
            self.state = new_state
            self.state_start_time = time.time()

        return self.state

    # Function that enforces hysteresis-based transitions
    def transition(self, a: float): 
        system_state = self.state
        match system_state :
            case state.CALM:
                if (a >= CALM_NEUTRAL_ENTER):
                    return state.NEUTRAL # Calm to Neutral
            case state.NEUTRAL:
                if (a <= NEUTRAL_CALM_EXIT):
                    return state.CALM # Neutral to Calm 
                if (a >= NEUTRAL_ENGAGED_ENTER):
                    return state.ENGAGED # Neutral to Engaged 
            case state.ENGAGED:
                if (a <= ENGAGED_NEUTRAL_EXIT):
                    return state.NEUTRAL # Engaged to Neutral
                if (a >= ENGAGED_OVERLOADED_ENTER):
                    return state.OVERLOADED # Engaged to Overloaded
            case state.OVERLOADED:
                if (a <= OVERLOADED_ENGAGED_EXIT):
                    return state.ENGAGED # Overloaded to Engaged 
            case _:
                action-default
        return system_state # No change