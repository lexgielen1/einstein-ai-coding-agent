#!/usr/bin/env python3
"""Text-to-speech helper (pyttsx3).

Optional: pipeline should still work if TTS is unavailable.
"""

from __future__ import annotations

from typing import Optional

_engine = None


def speak(text: str, rate: int = 190, voice_id: Optional[str] = None) -> None:
    global _engine

    try:
        import pyttsx3
    except Exception:
        return

    if _engine is None:
        _engine = pyttsx3.init()
        try:
            _engine.setProperty("rate", rate)
        except Exception:
            pass
        if voice_id:
            try:
                _engine.setProperty("voice", voice_id)
            except Exception:
                pass

    try:
        _engine.say(text)
        _engine.runAndWait()
    except Exception:
        return


if __name__ == "__main__":
    speak("Text to speech is working.")
