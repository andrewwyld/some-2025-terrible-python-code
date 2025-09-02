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

# then ramp up the frequency exponentially
# till the frequency reaches a final value

# then output the high frequency for an interval

# we need the ramp period to be fixed-ish independent of initial and final frequencies
# we need the initial and final frequencies to be related by a fixed factor

middle_C = 375 # middle C
middle_C_p5 = middle_C * 2 / 3
middle_C_8_9 = middle_C * 8 / 9
middle_C_16_27 = middle_C * 16 / 27
middle_C_64_81 = middle_C * 64 / 81
middle_C_128_243 = middle_C * 128 / 243
middle_C_512_729 = middle_C * 512 / 729
middle_C_2048_2187 = middle_C * 2048 / 2187
middle_C_4096_6561 = middle_C * 4096 / 6561
middle_C_16384_19683 = middle_C * 16384 / 19683
middle_C_32768_59049 = middle_C * 32768 / 59049
middle_C_131072_177147 = middle_C * 131072 / 177147
middle_C_524288_531441 = middle_C * 524288 / 531441

tw_root_2 = pow(2, 1/12)
sx_root_2 = pow(2, 1/6)
fr_root_2 = pow(2, 1/4)
th_root_2 = pow(2, 1/3)
root_2 = pow(2, 1/2)

middle_Cs = middle_C / tw_root_2 # 1/12
middle_D = middle_C / sx_root_2 # 2/12 = 1/6
middle_Ds = middle_C / fr_root_2 # 3/12 = 1/4
middle_E = middle_C / th_root_2 # 4/12 = 1/3
middle_F = middle_E / tw_root_2 # 5/12
middle_Fs = middle_C / root_2 # 6/12 = 1/2
middle_G = middle_Cs / root_2 # 7/12
middle_Gs = middle_E / th_root_2 # 8/12 = 2/3
upper_A = middle_Fs / fr_root_2  # 9/12 = 1/2 + 1/4
upper_As = middle_Gs / sx_root_2  # 10/12
upper_B = upper_As / tw_root_2

def generate(period: float, duration: float) -> np.typing.NDArray:
    length = math.floor(duration * samplerate)
    pw = math.floor(period / 2.0)
    output = np.zeros(length)
    cursor = 0
    while cursor < length:
        pulse_at(output, math.floor(cursor), pw, 1.0)
        cursor += period
    return output

def write(period: float, duration: float, name: str, root: np.typing.NDArray = None) -> np.typing.NDArray:
    current = generate(period, duration)

    audio_mono = np.array([current]).T
    audio_mono = (audio_mono * (2 ** 15 - 1)).astype("<h")

    with wave.open(name + ".wav", "w") as f:
        # 1 Channel
        f.setnchannels(1)
        # 2 bytes per sample.
        f.setsampwidth(2)
        f.setframerate(samplerate)
        f.writeframes(audio_mono.tobytes())

    if root is not None:
        audio_stereo = np.array([root, current]).T
        audio_stereo = (audio_stereo * (2 ** 15 - 1)).astype("<h")

        with wave.open(name + "_stereo.wav", "w") as f:
            # 2 Channels.
            f.setnchannels(2)
            # 2 bytes per sample.
            f.setsampwidth(2)
            f.setframerate(samplerate)
            f.writeframes(audio_stereo.tobytes())

    return current

root = write(middle_C, 1.0, "middle_C")

write(middle_C_p5, 1.0, "middle_C_p5", root)
write(middle_C_8_9, 1.0, "middle_C_8_9", root)
write(middle_C_16_27, 1.0, "middle_C_16_27", root)
write(middle_C_64_81, 1.0, "middle_C_64_81", root)
write(middle_C_128_243, 1.0, "middle_C_128_243", root)
write(middle_C_512_729, 1.0, "middle_C_512_729", root)
write(middle_C_2048_2187, 1.0, "middle_C_2048_2187", root)
write(middle_C_4096_6561, 1.0, "middle_C_4096_6561", root)
write(middle_C_16384_19683, 1.0, "middle_C_16384_19683", root)
write(middle_C_32768_59049, 1.0, "middle_C_32768_59049", root)
write(middle_C_131072_177147, 1.0, "middle_C_131072_177147", root)
write(middle_C_524288_531441, 1.0, "middle_C_524288_531441", root)

write(middle_Cs, 1.0, "middle_Cs", root)
write(middle_D, 1.0, "middle_D")
write(middle_Ds, 1.0, "middle_Ds")
write(middle_E, 1.0, "middle_E")
write(middle_F, 1.0, "middle_F")
write(middle_Fs, 1.0, "middle_Fs")
write(middle_G, 1.0, "middle_G")
write(middle_Gs, 1.0, "middle_Gs")
write(upper_A, 1.0, "upper_A")
write(upper_As, 1.0, "upper_As")
write(upper_B, 1.0, "upper_B")