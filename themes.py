THEMES = {
    "dark": {
        "background_color": "#0E1117",
        "text_color": "#FAFAFA",
        "primary_color": "#4CAF50",
        "secondary_color": "#2196F3",
        "accent_color": "#FF4081",
        "theme_colors": {
            "primary_color": "#4CAF50",
            "secondary_color": "#2196F3",
            "accent_color": "#FF4081",
            "background_color": "#0E1117"
        },
        "css": """
            .stButton > button {
                border-color: rgba(255, 255, 255, 0.1);
                background-color: rgba(76, 175, 80, 0.1);
            }
            .story-text {
                background-color: rgba(255, 255, 255, 0.05);
                border-left: 4px solid #4CAF50;
            }
        """
    },
    "light": {
        "background_color": "#FFFFFF",
        "text_color": "#212121",
        "primary_color": "#4CAF50",
        "secondary_color": "#2196F3",
        "accent_color": "#FF4081",
        "theme_colors": {
            "primary_color": "#4CAF50",
            "secondary_color": "#2196F3",
            "accent_color": "#FF4081",
            "background_color": "#FFFFFF"
        },
        "css": """
            .stButton > button {
                border-color: rgba(0, 0, 0, 0.1);
                background-color: rgba(76, 175, 80, 0.1);
            }
            .story-text {
                background-color: rgba(0, 0, 0, 0.05);
                border-left: 4px solid #4CAF50;
            }
        """
    },
    "mystery": {
        "background_color": "#1A1A2E",
        "text_color": "#E0E0E0",
        "primary_color": "#722F37",
        "secondary_color": "#4A1B1F",
        "accent_color": "#D4AF37",
        "theme_colors": {
            "primary_color": "#722F37",
            "secondary_color": "#4A1B1F",
            "accent_color": "#D4AF37",
            "background_color": "#1A1A2E"
        },
        "css": """
            .stButton > button {
                border-color: rgba(212, 175, 55, 0.2);
                background-color: rgba(114, 47, 55, 0.1);
            }
            .stButton > button:hover {
                border-color: rgba(212, 175, 55, 0.4);
                background-color: rgba(114, 47, 55, 0.2);
            }
            .story-text {
                background-color: rgba(74, 27, 31, 0.2);
                border-left: 4px solid #722F37;
            }
        """
    }
}

SOUND_EFFECTS = {
    "button_click": "Basic interaction sound",
    "story_end": "Story completion sound",
    "badge_earned": "Achievement unlocked sound",
    "theme_change": "Theme switching sound",
    "mystery_ambient": "Background ambiance for mystery theme"
}