import os
import logging
from pathlib import Path

class AudioManager:
    def __init__(self):
        self.sounds_dir = Path("assets/sounds")
        self.sounds_dir.mkdir(parents=True, exist_ok=True)
        self.volume = 0.7
        self._stop_flag = False
        logging.info("Audio functionality is disabled in cloud deployment")

    def set_volume(self, volume: float):
        """Set volume level (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))

    def narrate(self, text: str, lang='en', speed=False) -> bool:
        """Stub for text-to-speech narration"""
        logging.info(f"Narration disabled: {text[:50]}...")
        return True

    def play_sound_effect(self, effect_name: str) -> None:
        """Stub for playing sound effects"""
        logging.info(f"Sound effect disabled: {effect_name}")
        return None

    def play_background_music(self, music_name: str, loop: bool = True) -> None:
        """Stub for playing background music"""
        logging.info(f"Background music disabled: {music_name}")

    def stop_background_music(self) -> None:
        """Stub for stopping background music"""
        self._stop_flag = True

    def stop(self) -> None:
        """Stub for stopping all audio"""
        self._stop_flag = True