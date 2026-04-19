#!/usr/bin/env python3
"""Wake word detection using Porcupine.

Note: Free built-in keywords are limited. We use 'jarvis' as default.
"""

from __future__ import annotations

import struct
from typing import Optional


def wait_for_wake_word(keyword: str = "jarvis", sensitivity: float = 0.6) -> bool:
    """Block until wake word detected. Returns True when detected."""

    import pvporcupine
    import pyaudio

    porcupine = pvporcupine.create(keywords=[keyword], sensitivities=[sensitivity])
    pa = pyaudio.PyAudio()

    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length,
    )

    print(f"👂 Listening for wake word: '{keyword}' ...")

    try:
        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print("✅ Wake word detected!")
                return True
    except KeyboardInterrupt:
        return False
    finally:
        try:
            audio_stream.close()
        except Exception:
            pass
        try:
            pa.terminate()
        except Exception:
            pass
        try:
            porcupine.delete()
        except Exception:
            pass


if __name__ == "__main__":
    wait_for_wake_word()
