
import numpy as np
from scipy.io.wavfile import write
import os

os.makedirs("sounds", exist_ok=True)

rate = 44100
duration = 0.35

drums = {
    "left": 110,
    "center": 180,
    "right": 250
}

for name, frequency in drums.items():
    t = np.linspace(0, duration, int(rate * duration))
    sound = (
        np.sin(2 * np.pi * frequency * t) * np.exp(-12 * t)
        + 0.4 * np.sin(2 * np.pi * frequency * 2 * t) * np.exp(-18 * t)
        + 0.15 * np.random.randn(len(t)) * np.exp(-25 * t)
    )

    sound = sound / np.max(np.abs(sound))
    sound = (sound * 32767).astype(np.int16)

    write(f"sounds/{name}.wav", rate, sound)

print("Improved drum sounds created!")