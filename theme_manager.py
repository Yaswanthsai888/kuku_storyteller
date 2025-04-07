import streamlit as st
from themes import THEMES, SOUND_EFFECTS
from pathlib import Path

class ThemeManager:
    def __init__(self, audio_manager):
        self.audio_manager = audio_manager
        self.current_theme = "dark"
        self.current_mood = "mysterious"
        self._setup_theme_assets()
        self._init_mood_sounds()

    def _setup_theme_assets(self):
        """Setup theme asset directories"""
        assets_dir = Path("assets")
        assets_dir.mkdir(exist_ok=True)
        sounds_dir = assets_dir / "sounds"
        sounds_dir.mkdir(exist_ok=True)

    def _init_mood_sounds(self):
        """Initialize mood-specific sound mappings"""
        self.mood_sounds = {
            "mysterious": "mystery_ambient",
            "tense": "tense_ambient",
            "peaceful": "peaceful_ambient",
            "dramatic": "dramatic_ambient"
        }

    def apply_theme(self, theme_name, transition=True):
        """Apply visual and audio theme with smooth transitions"""
        if theme_name not in THEMES:
            theme_name = "dark"
        
        prev_theme = self.current_theme
        self.current_theme = theme_name
        theme = THEMES[theme_name]
        
        # Visual theme application
        st.markdown(f"""
            <style>
                /* Theme base styles */
                {theme['css']}
                
                /* Theme transitions */
                .stApp {{
                    background-color: {theme['background_color']};
                    color: {theme['text_color']};
                    transition: all 0.5s ease-in-out;
                }}
                
                /* Enhanced theme-specific elements */
                .theme-card {{
                    background: {theme['primary_color']}11;
                    border: 2px solid {theme['primary_color']}22;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px 0;
                    backdrop-filter: blur(10px);
                    transition: all 0.3s ease-in-out;
                }}
                
                .theme-card:hover {{
                    border-color: {theme['primary_color']}44;
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px {theme['primary_color']}11;
                }}
                
                /* Theme-aware progress bars */
                .stProgress > div > div {{
                    background: linear-gradient(
                        90deg,
                        {theme['primary_color']},
                        {theme['accent_color']}
                    );
                }}
            </style>
        """, unsafe_allow_html=True)

        # Audio transition
        if transition and prev_theme != theme_name:
            self.play_effect("theme_change")
            if theme_name == "mystery":
                self.audio_manager.play_background_music("mystery_ambient", loop=True)
            else:
                self.audio_manager.stop_background_music()

    def apply_mood(self, mood: str):
        """Apply mood-specific effects and sounds"""
        if mood != self.current_mood:
            self.current_mood = mood
            
            # Stop current mood sound if playing
            self.audio_manager.stop_background_music()
            
            # Play new mood sound if available
            if mood in self.mood_sounds:
                self.audio_manager.play_background_music(
                    self.mood_sounds[mood],
                    loop=True
                )

    def play_effect(self, effect_name: str):
        """Play a theme-aware sound effect"""
        if effect_name in SOUND_EFFECTS:
            self.audio_manager.play_sound_effect(effect_name)

    def get_theme_color(self, color_name: str) -> str:
        """Get a specific color from current theme"""
        theme = THEMES[self.current_theme]
        return theme.get(color_name, theme.get('primary_color'))

    def get_theme_colors(self) -> dict:
        """Get all theme colors"""
        return THEMES[self.current_theme]["theme_colors"]

    def get_current_theme(self) -> str:
        """Get current theme name"""
        return self.current_theme

    def get_current_mood(self) -> str:
        """Get current mood name"""
        return self.current_mood