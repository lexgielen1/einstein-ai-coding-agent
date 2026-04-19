#!/usr/bin/env python3
"""Einstein AI Coding Agent - Prototype MVP (Studio)

Optional add-ons:
- Wake word (Porcupine)
- TTS confirmations (pyttsx3)

Run without mic:
  python3 test_pipeline_no_mic.py

Run interactive:
  python3 main.py
  python3 main.py --wake-word --tts
"""

from __future__ import annotations

import argparse

from voice.listener import VoiceListener
from llm.coder import generate_code
from executor.runner import execute_code
from storage.manager import save_code


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--wake-word", action="store_true", help="Wait for wake word before listening")
    p.add_argument("--tts", action="store_true", help="Speak short confirmations")
    p.add_argument("--typed", action="store_true", help="Force typed input (no microphone)")
    p.add_argument("--wake-keyword", default="jarvis", help="Porcupine built-in keyword (default: jarvis)")
    args = p.parse_args()

    speaker = None
    if args.tts:
        try:
            from voice.tts import speak

            speaker = speak
        except Exception:
            speaker = None

    if args.wake_word:
        try:
            from voice.wake_word import wait_for_wake_word

            ok = wait_for_wake_word(keyword=args.wake_keyword)
            if not ok:
                return 1
        except Exception as e:
            print(f"⚠️ Wake word unavailable: {e}")

    listener = VoiceListener(prefer_voice=not args.typed)
    command = listener.listen()
    if not command:
        print("❌ No command")
        return 1

    print(f"\n📝 Task: {command}\n")
    if speaker:
        speaker("Generating code")

    code = generate_code(command)
    if not code:
        print("❌ Code generation failed")
        if speaker:
            speaker("Code generation failed")
        return 1

    file_path = save_code(code, command)
    result = execute_code(code)

    ok = bool(result.get("success"))
    if ok:
        print("\n✅ Done")
        if speaker:
            speaker("Done")
    else:
        print("\n❌ Execution failed")
        if speaker:
            speaker("Execution failed")

    print(f"📁 Saved: {file_path}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
