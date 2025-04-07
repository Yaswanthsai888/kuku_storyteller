import os
from gtts import gTTS
from playsound import playsound
import tempfile
import threading
from pathlib import Path
import numpy as np
import wave
import logging

class AudioManager:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.current_playback = None
        self.background_music = None
        self._stop_flag = False
        self.sounds_dir = Path("assets/sounds")
        self.sounds_dir.mkdir(parents=True, exist_ok=True)
        self.volume = 0.7
        self._active_playbacks = set()
        self._lock = threading.Lock()

    def set_volume(self, volume: float):
        """Set volume level (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))

    def narrate(self, text: str, lang='en', speed=False) -> bool:
        """Convert text to speech and play it"""
        try:
            # Stop any existing narration
            self.stop()
            
            # Generate audio file
            tts = gTTS(text=text, lang=lang, slow=speed)
            temp_file = os.path.join(self.temp_dir, 'narration.mp3')
            tts.save(temp_file)
            
            # Play in a separate thread to not block the UI
            thread = threading.Thread(target=self._play_audio, args=(temp_file,))
            thread.daemon = True
            thread.start()
            return True
        except Exception as e:
            logging.error(f"Error in narration: {e}")
            return False

    def play_sound_effect(self, effect_name: str) -> None:
        """Play a sound effect from the sounds directory"""
        try:
            with self._lock:
                effect_path = self.sounds_dir / f"{effect_name}.wav"
                if effect_path.exists():
                    thread = threading.Thread(target=playsound, args=(str(effect_path),))
                    thread.daemon = True
                    thread.start()
                    self._active_playbacks.add(thread)
                    return thread
        except Exception as e:
            logging.error(f"Error playing sound effect: {e}")
        return None

    def play_background_music(self, music_name: str, loop: bool = True) -> None:
        """Play background music with optional looping"""
        try:
            self.stop_background_music()
            
            with self._lock:
                music_path = self.sounds_dir / f"{music_name}.wav"
                if music_path.exists():
                    def _loop_playback():
                        while not self._stop_flag:
                            playsound(str(music_path))
                            if not loop:
                                break
                    
                    thread = threading.Thread(target=_loop_playback)
                    thread.daemon = True
                    thread.start()
                    self.background_music = thread
                    self._active_playbacks.add(thread)
        except Exception as e:
            logging.error(f"Error playing background music: {e}")

    def stop_background_music(self) -> None:
        """Stop the currently playing background music"""
        with self._lock:
            if self.background_music:
                self._stop_flag = True
                if self.background_music in self._active_playbacks:
                    self._active_playbacks.remove(self.background_music)
                self.background_music = None

    def stop(self) -> None:
        """Stop all audio playback"""
        with self._lock:
            self._stop_flag = True
            if self.current_playback:
                self.current_playback.join(timeout=1)
            self.stop_background_music()
            
            # Stop all active playbacks
            for playback in list(self._active_playbacks):
                try:
                    playback.join(timeout=1)
                except:
                    pass
            self._active_playbacks.clear()
            self._stop_flag = False

    def _play_audio(self, file_path: str) -> None:
        """Play audio file"""
        try:
            thread = threading.Thread(target=playsound, args=(file_path,))
            thread.daemon = True
            with self._lock:
                self.current_playback = thread
                self._active_playbacks.add(thread)
            thread.start()
            thread.join()
        except Exception as e:
            logging.error(f"Error playing audio: {e}")
        finally:
            with self._lock:
                if self.current_playback in self._active_playbacks:
                    self._active_playbacks.remove(self.current_playback)
                self.current_playback = None
            self._stop_flag = False

    def __del__(self):
        """Cleanup when the object is destroyed"""
        self.stop()
        try:
            # Clean up temporary directory
            if os.path.exists(self.temp_dir):
                for file in os.listdir(self.temp_dir):
                    os.remove(os.path.join(self.temp_dir, file))
                os.rmdir(self.temp_dir)
        except:
            pass