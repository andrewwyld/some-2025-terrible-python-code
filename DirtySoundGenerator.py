import wave
import math
import numpy as np

samplerate = 96000

def pulse_at(array: np.typing.NDArray, position: int, pulse_width: int, pulse_height: float) -> np.typing.NDArray:
    # if position is out of bounds do nothing
    if position >= len(array):
        return array

    # otherwise insult a pulse at this position
    for sample in range(position, min(position + pulse_width, len(array))):
        array[sample] = pulse_height
    return array

def shift_factor(period_ratio: float, click_ratio: float) -> float:
    return math.pow(decrement, click_ratio * (math.log(period_ratio, 2)))

constant_interval = 10
final_time = 25

start_period_base = 48000
end_period_base = 375 # middle C

decrement = 0.99

def logdiff(start_value: float, start_period: float, end_period: float, step: float) -> float:
    return start_value * start_period * (math.log(step + 1) - math.log(step))

def make_noise(start_period: float, end_period: float) -> np.typing.NDArray:
    pw = end_period * 0.5
    cursor = 0
    start_pos = 2 * samplerate / start_period
    channel = np.zeros(samplerate * (constant_interval + final_time))

    # first do pulses according to the initial period
    while cursor < constant_interval * samplerate:
        pulse_at(channel, math.floor(cursor), math.floor(pw), 1.0)
        cursor += start_period

    period = start_period
    pos = start_pos

    while period > end_period:
        pulse_at(channel, math.floor(cursor), math.floor(pw), 1.0)
        period = logdiff(start_pos, start_period, end_period, pos)
        cursor += period
        pos += 1

    period = end_period

    while cursor < len(channel):
        pulse_at(channel, math.floor(cursor), math.floor(pw), 1.0)
        cursor += period

    return channel

def record(start_period: float, end_period: float, name: str) -> None:
    ramp = make_noise(start_period, end_period)
    audio_ramp = np.array([ramp]).T
    audio_ramp = (audio_ramp * (2 ** 15 - 1)).astype("<h")

    with wave.open(name + ".wav", "w") as f:
        f.setnchannels(1)  # mono
        # 2 bytes per sample.
        f.setsampwidth(2)
        f.setframerate(samplerate)
        f.writeframes(audio_ramp.tobytes())

record(start_period_base, end_period_base, "ramp_mid_C")
record(start_period_base / 1.5, end_period_base / 1.5, "ramp_mid_G")
record(start_period_base / 2, end_period_base / 2, "ramp_hi_C")
record(start_period_base / 3, end_period_base / 3, "ramp_hi_G")
