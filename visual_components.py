import streamlit as st
from typing import Dict, Any

def apply_cursor_theme(theme_name: str):
    """Apply a custom cursor based on theme"""
    cursors = {
        "mystery": """
            * { cursor: url("data:image/svg+xml,%3Csvg width='32' height='32' viewBox='0 0 32 32' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='16' cy='16' r='8' stroke='%23D4AF37' stroke-width='2'/%3E%3C/svg%3E") 16 16, auto; }
            .stButton > button { cursor: pointer; }
        """,
        "dark": """
            * { cursor: url("data:image/svg+xml,%3Csvg width='32' height='32' viewBox='0 0 32 32' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='16' cy='16' r='8' stroke='%234CAF50' stroke-width='2'/%3E%3C/svg%3E") 16 16, auto; }
            .stButton > button { cursor: pointer; }
        """,
        "light": """
            * { cursor: url("data:image/svg+xml,%3Csvg width='32' height='32' viewBox='0 0 32 32' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='16' cy='16' r='8' stroke='%232196F3' stroke-width='2'/%3E%3C/svg%3E") 16 16, auto; }
            .stButton > button { cursor: pointer; }
        """
    }
    
    st.markdown(f"<style>{cursors.get(theme_name, cursors['dark'])}</style>", unsafe_allow_html=True)

def mood_indicator(mood: str, theme_colors: Dict[str, Any]):
    """Display a visual indicator of the scene's mood"""
    mood_colors = {
        "tense": "#FF5722",
        "mysterious": "#9C27B0",
        "peaceful": "#4CAF50",
        "dramatic": "#D4AF37"
    }
    
    mood_animations = {
        "tense": "shake 0.5s infinite",
        "mysterious": "glow 2s infinite",
        "peaceful": "float 3s infinite",
        "dramatic": "pulse 1.5s infinite"
    }
    
    mood_icons = {
        "tense": "⚡",
        "mysterious": "🔍",
        "peaceful": "🌟",
        "dramatic": "🎭"
    }
    
    st.markdown(f"""
        <style>
            @keyframes shake {{
                0%, 100% {{ transform: translateX(0); }}
                25% {{ transform: translateX(-3px); }}
                75% {{ transform: translateX(3px); }}
            }}
            
            @keyframes glow {{
                0%, 100% {{ filter: brightness(1) drop-shadow(0 0 5px {mood_colors.get(mood, theme_colors['primary_color'])}66); }}
                50% {{ filter: brightness(1.3) drop-shadow(0 0 10px {mood_colors.get(mood, theme_colors['primary_color'])}99); }}
            }}
            
            @keyframes float {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-5px); }}
            }}
            
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.1); }}
            }}
            
            .mood-indicator {{
                position: fixed;
                top: 20px;
                right: 20px;
                background-color: {mood_colors.get(mood, theme_colors['primary_color'])}22;
                padding: 10px 20px;
                border-radius: 20px;
                backdrop-filter: blur(5px);
                border: 2px solid {mood_colors.get(mood, theme_colors['primary_color'])}44;
                animation: {mood_animations.get(mood, "pulse 2s infinite")};
                z-index: 1000;
                transition: all 0.3s ease-in-out;
            }}
            
            .mood-indicator:hover {{
                transform: scale(1.05);
                background-color: {mood_colors.get(mood, theme_colors['primary_color'])}33;
            }}
        </style>
        <div class="mood-indicator">
            <span style="
                font-size: 1.2em;
                color: {mood_colors.get(mood, theme_colors['primary_color'])};
            ">
                {mood_icons.get(mood, "📖")} {mood.title()}
            </span>
        </div>
    """, unsafe_allow_html=True)

def scene_transition(direction="forward"):
    """Create a smooth transition effect between scenes"""
    transition_css = """
        <style>
            @keyframes slideIn {
                from { 
                    transform: translateX(100%);
                    opacity: 0;
                    filter: blur(10px);
                }
                to { 
                    transform: translateX(0);
                    opacity: 1;
                    filter: blur(0);
                }
            }
            @keyframes slideOut {
                from { 
                    transform: translateX(0);
                    opacity: 1;
                    filter: blur(0);
                }
                to { 
                    transform: translateX(-100%);
                    opacity: 0;
                    filter: blur(10px);
                }
            }
            .slide-in {
                animation: slideIn 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            }
            .slide-out {
                animation: slideOut 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            }
        </style>
    """
    st.markdown(transition_css, unsafe_allow_html=True)
    return "slide-in" if direction == "forward" else "slide-out"

def apply_ambient_background(mood: str, theme_colors: Dict[str, Any]):
    """Create an ambient background effect based on scene mood"""
    mood_gradients = {
        "tense": f"""
            background: linear-gradient(45deg, 
                {theme_colors['primary_color']}15 25%, 
                {theme_colors['accent_color']}15 75%
            );
            animation: tensePulse 4s ease-in-out infinite;
        """,
        "mysterious": f"""
            background: radial-gradient(circle at 50% 50%,
                {theme_colors['background_color']} 0%,
                {theme_colors['primary_color']}15 100%
            );
            animation: mysteryFade 8s ease-in-out infinite;
        """,
        "peaceful": f"""
            background: linear-gradient(135deg,
                {theme_colors['primary_color']}10,
                {theme_colors['secondary_color']}10
            );
            animation: peacefulWave 10s ease-in-out infinite;
        """,
        "dramatic": f"""
            background: linear-gradient(90deg,
                {theme_colors['accent_color']}20,
                {theme_colors['primary_color']}20
            );
            animation: dramaticPulse 3s ease-in-out infinite;
        """
    }
    
    st.markdown(f"""
        <style>
            @keyframes tensePulse {{
                0%, 100% {{ background-position: 0% 0%; filter: hue-rotate(0deg); }}
                50% {{ background-position: 100% 100%; filter: hue-rotate(15deg); }}
            }}
            
            @keyframes mysteryFade {{
                0%, 100% {{ opacity: 0.7; filter: brightness(0.9); }}
                50% {{ opacity: 1; filter: brightness(1.1); }}
            }}
            
            @keyframes peacefulWave {{
                0%, 100% {{ 
                    background-size: 200% 200%;
                    filter: brightness(1) blur(0px);
                }}
                50% {{ 
                    background-size: 150% 150%;
                    filter: brightness(1.1) blur(1px);
                }}
            }}
            
            @keyframes dramaticPulse {{
                0%, 100% {{ 
                    transform: scale(1);
                    filter: contrast(1);
                }}
                50% {{ 
                    transform: scale(1.05);
                    filter: contrast(1.1);
                }}
            }}
            
            .stApp {{
                {mood_gradients.get(mood, mood_gradients['mysterious'])}
                transition: background 1s ease-in-out;
            }}
        </style>
    """, unsafe_allow_html=True)

def scene_particles(mood: str):
    """Add dynamic particle effects based on scene mood"""
    particle_configs = {
        "mysterious": {
            "color": "#D4AF37",
            "size": "4px",
            "count": 50,
            "speed": 2,
            "blur": "2px",
            "opacity": 0.6
        },
        "tense": {
            "color": "#FF5722",
            "size": "3px",
            "count": 30,
            "speed": 4,
            "blur": "1px",
            "opacity": 0.7
        },
        "peaceful": {
            "color": "#4CAF50",
            "size": "5px",
            "count": 20,
            "speed": 1,
            "blur": "3px",
            "opacity": 0.5
        },
        "dramatic": {
            "color": "#9C27B0",
            "size": "4px",
            "count": 40,
            "speed": 3,
            "blur": "2px",
            "opacity": 0.6
        }
    }
    
    config = particle_configs.get(mood, particle_configs["mysterious"])
    
    st.markdown(f"""
        <style>
            @keyframes float-particle {{
                0% {{
                    transform: translateY(100vh) translateX(0) rotate(0deg);
                    opacity: 0;
                }}
                20% {{
                    opacity: {config['opacity']};
                }}
                80% {{
                    opacity: {config['opacity']};
                }}
                100% {{
                    transform: translateY(-100px) translateX(100px) rotate(360deg);
                    opacity: 0;
                }}
            }}
            
            .particle {{
                position: fixed;
                width: {config['size']};
                height: {config['size']};
                background: {config['color']};
                border-radius: 50%;
                pointer-events: none;
                opacity: 0;
                z-index: 0;
                filter: blur({config['blur']});
                box-shadow: 0 0 10px {config['color']}66;
            }}
        </style>
        
        <script>
            function createParticle() {{
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * window.innerWidth + 'px';
                particle.style.animation = `float-particle ${{3 + Math.random() * 4}}s linear`;
                document.body.appendChild(particle);
                
                particle.addEventListener('animationend', () => {{
                    particle.remove();
                }});
            }}
            
            // Clear existing particles
            document.querySelectorAll('.particle').forEach(p => p.remove());
            
            // Create new particles
            setInterval(createParticle, {1000 / config['speed']});
        </script>
    """, unsafe_allow_html=True)

def scene_filter(mood: str):
    """Apply a dynamic visual filter effect based on scene mood"""
    filter_effects = {
        "mysterious": {
            "base": "brightness(0.9) contrast(1.1)",
            "hover": "brightness(1) contrast(1.15) saturate(1.1)"
        },
        "tense": {
            "base": "brightness(0.85) contrast(1.2) saturate(1.1)",
            "hover": "brightness(0.9) contrast(1.25) saturate(1.2)"
        },
        "peaceful": {
            "base": "brightness(1.05) contrast(0.95) saturate(0.95)",
            "hover": "brightness(1.1) contrast(1) saturate(1)"
        },
        "dramatic": {
            "base": "brightness(0.95) contrast(1.15) saturate(1.2)",
            "hover": "brightness(1) contrast(1.2) saturate(1.3)"
        }
    }
    
    effect = filter_effects.get(mood, filter_effects["mysterious"])
    
    st.markdown(f"""
        <style>
            .stApp {{
                filter: {effect['base']};
                transition: filter 1s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            
            .story-text:hover {{
                filter: {effect['hover']};
            }}
        </style>
    """, unsafe_allow_html=True)