#!/usr/bin/env python3
"""prototype.voice.listener

Voice input module.

Design goals for the prototype:
- Prefer real microphone + Whisper STT when dependencies are present.
- Degrade gracefully to typed input when audio deps are missing (CI, headless).

This keeps the whole pipeline runnable without forcing PyAudio / microphone access.
"""

from __future__ import annotations

from typing import Optional

try:
    import speech_recognition as sr  # type: ignore
except Exception:  # pragma: no cover
    sr = None  # type: ignore


class VoiceListener:
    """Handles voice input capture and transcription"""
    
    def __init__(
        self,
        prefer_voice: bool = True,
        whisper_model: str = "base",
        language: str = "english",
    ):
        """Initialize the voice listener.

        Args:
            prefer_voice: If True and audio deps are available, use microphone.
            whisper_model: Whisper model name used by SpeechRecognition.
            language: Whisper language hint used by SpeechRecognition.
        """
        self.prefer_voice = prefer_voice
        self.whisper_model = whisper_model
        self.language = language

        self._sr_available = sr is not None
        self.recognizer = None
        if self._sr_available:
            self.recognizer = sr.Recognizer()
            # Sensible defaults, dynamic threshold adapts to environment.
            self.recognizer.energy_threshold = 4000
            self.recognizer.dynamic_energy_threshold = True
        
    def listen(self) -> Optional[str]:
        """
        Listen for voice command after ENTER key press
        
        Returns:
            str: Transcribed command text, or None if failed
        """
        if self.prefer_voice and self._sr_available:
            return self._listen_microphone()
        return self._listen_text()

    def _listen_text(self) -> Optional[str]:
        """Fallback input mode (typed command)."""
        try:
            print("\n⌨️  Type your request (fallback mode).")
            text = input("> ").strip()
            return text or None
        except (EOFError, KeyboardInterrupt):
            return None

    def _listen_microphone(self) -> Optional[str]:
        """Record audio from microphone and transcribe with Whisper via SpeechRecognition."""
        assert sr is not None and self.recognizer is not None

        print("\n🎤 Press ENTER when ready to speak...")
        input()  # Wait for ENTER key

        print("🔴 Recording (5 seconds)...")

        try:
            with sr.Microphone() as source:
                print("   Calibrating microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

                print("   Speak now!")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)

                print("⚙️  Transcribing...")

                # Transcribe using Whisper (local model). SpeechRecognition exposes
                # recognize_whisper if whisper is installed.
                if not hasattr(self.recognizer, "recognize_whisper"):
                    raise RuntimeError(
                        "SpeechRecognition Whisper support not available. "
                        "Install openai-whisper and use a SpeechRecognition version that supports recognize_whisper."
                    )

                try:
                    text = self.recognizer.recognize_whisper(
                        audio,
                        model=self.whisper_model,
                        language=self.language,
                    )
                    print(f"✅ Transcribed: '{text}'")
                    return text.strip()
                except sr.UnknownValueError:
                    print("❌ Could not understand audio")
                    return None

        except sr.WaitTimeoutError:
            print("❌ No speech detected (timeout)")
            return None

        except Exception as e:
            print(f"❌ Error during recording/transcription: {e}")
            return None
    
    def test_microphone(self) -> bool:
        """
        Test if microphone is available
        
        Returns:
            bool: True if microphone works
        """
        if not self._sr_available:
            print("⚠️  speech_recognition not installed, microphone unavailable (fallback to typed input)")
            return False
        try:
            mic_list = sr.Microphone.list_microphone_names()  # type: ignore[attr-defined]
            print(f"📢 Available microphones ({len(mic_list)}):")
            for i, name in enumerate(mic_list):
                print(f"   [{i}] {name}")
            return len(mic_list) > 0
        except Exception as e:
            print(f"❌ Microphone test failed: {e}")
            return False


def main():
    """Test the voice listener"""
    print("Voice Listener Test")
    print("=" * 50)
    
    listener = VoiceListener()
    
    # Test microphone
    if not listener.test_microphone():
        print("❌ No microphone available!")
        return
    
    print("\n✅ Microphone ready")
    
    # Test voice capture
    while True:
        command = listener.listen()
        
        if command:
            print(f"\n✅ Got command: {command}")
        else:
            print("\n❌ Failed to capture command")
        
        print("\nPress Ctrl+C to exit, or continue...")
        

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
