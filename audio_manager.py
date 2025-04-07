import os
from gtts import gTTS
import simpleaudio as sa
import tempfile
import threading
from pathlib import Path
import numpy as np
import wave

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

    def _adjust_volume(self, audio_data, volume):
        """Adjust the volume of audio data"""
        return (audio_data * volume).astype(np.int16)

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
            print(f"Error in narration: {e}")
            return False

    def play_sound_effect(self, effect_name: str) -> sa.PlayObject:
        """Play a sound effect from the sounds directory"""
        try:
            with self._lock:
                effect_path = self.sounds_dir / f"{effect_name}.wav"
                if effect_path.exists():
                    audio_data = self._load_and_adjust_volume(str(effect_path))
                    play_obj = sa.play_buffer(audio_data, 1, 2, 44100)
                    self._active_playbacks.add(play_obj)
                    return play_obj
        except Exception as e:
            print(f"Error playing sound effect: {e}")
        return None

    def play_background_music(self, music_name: str, loop: bool = True) -> None:
        """Play background music with optional looping"""
        try:
            self.stop_background_music()
            
            with self._lock:
                music_path = self.sounds_dir / f"{music_name}.wav"
                if music_path.exists():
                    audio_data = self._load_and_adjust_volume(str(music_path))
                    self.background_music = sa.play_buffer(audio_data, 1, 2, 44100)
                    self._active_playbacks.add(self.background_music)
                    
                    if loop:
                        def _loop_playback():
                            while not self._stop_flag and self.background_music:
                                if not self.background_music.is_playing():
                                    with self._lock:
                                        if self.background_music in self._active_playbacks:
                                            self._active_playbacks.remove(self.background_music)
                                        self.background_music = sa.play_buffer(audio_data, 1, 2, 44100)
                                        self._active_playbacks.add(self.background_music)
                        
                        thread = threading.Thread(target=_loop_playback)
                        thread.daemon = True
                        thread.start()
        except Exception as e:
            print(f"Error playing background music: {e}")

    def _load_and_adjust_volume(self, file_path: str) -> np.ndarray:
        """Load and adjust volume of a WAV file"""
        try:
            if not os.path.exists(file_path):
                print(f"Audio file not found: {file_path}")
                return np.zeros(0, dtype=np.int16)
                
            with wave.open(file_path, 'rb') as wave_file:
                n_frames = wave_file.getnframes()
                audio_data = wave_file.readframes(n_frames)
                audio_array = np.frombuffer(audio_data, dtype=np.int16)
                adjusted_audio = self._adjust_volume(audio_array, self.volume)
                return adjusted_audio
        except Exception as e:
            print(f"Error loading audio file {file_path}: {e}")
            return np.zeros(0, dtype=np.int16)

    def stop_background_music(self) -> None:
        """Stop the currently playing background music"""
        with self._lock:
            if self.background_music:
                if self.background_music in self._active_playbacks:
                    self._active_playbacks.remove(self.background_music)
                self.background_music.stop()
                self.background_music = None

    def stop(self) -> None:
        """Stop all audio playback"""
        with self._lock:
            self._stop_flag = True
            if self.current_playback:
                self.current_playback.stop()
            self.stop_background_music()
            
            # Stop all active playbacks
            for playback in list(self._active_playbacks):
                try:
                    playback.stop()
                except:
                    pass
            self._active_playbacks.clear()
            self._stop_flag = False

    def _play_audio(self, file_path: str) -> None:
        """Play audio file"""
        try:
            audio_data = self._load_and_adjust_volume(file_path)
            with self._lock:
                self.current_playback = sa.play_buffer(audio_data, 1, 2, 44100)
                self._active_playbacks.add(self.current_playback)
            self.current_playback.wait_done()
        except Exception as e:
            print(f"Error playing audio: {e}")
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
                os.rmdir(self.temp_dir)
        except:
            pass