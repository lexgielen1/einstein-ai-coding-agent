#!/usr/bin/env python3
"""
Voice Input Module - Captures and transcribes voice commands
Uses ENTER key activation (simpler than wake word for MVP)
"""

import speech_recognition as sr
from typing import Optional
import time


class VoiceListener:
    """Handles voice input capture and transcription"""
    
    def __init__(self):
        """Initialize the voice listener with Whisper STT"""
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000  # Adjust based on environment
        self.recognizer.dynamic_energy_threshold = True
        
    def listen(self) -> Optional[str]:
        """
        Listen for voice command after ENTER key press
        
        Returns:
            str: Transcribed command text, or None if failed
        """
        print("\n🎤 Press ENTER when ready to speak...")
        input()  # Wait for ENTER key
        
        print("🔴 Recording (5 seconds)...")
        
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                print("   Calibrating microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Record audio (5 second timeout)
                print("   Speak now!")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
                print("⚙️  Transcribing...")
                
                # Transcribe using Whisper (local model)
                try:
                    text = self.recognizer.recognize_whisper(
                        audio, 
                        model="base",  # Options: tiny, base, small, medium, large
                        language="english"
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
            print(f"❌ Error during recording: {e}")
            return None
    
    def test_microphone(self) -> bool:
        """
        Test if microphone is available
        
        Returns:
            bool: True if microphone works
        """
        try:
            mic_list = sr.Microphone.list_microphone_names()
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
