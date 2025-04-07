# app.py

import streamlit as st
from kuku_buddy import KukuBuddy
from memory_manager import MemoryManager
from audio_manager import AudioManager
from theme_manager import ThemeManager
from openai_manager import OpenAIManager
from components.interactive import typing_effect, animated_choice_buttons
from components.stats_view import display_achievements, display_story_stats
from audio_components import NarrationProgress, audio_settings
from visual_components import (
    apply_cursor_theme, 
    mood_indicator, 
    scene_transition,
    apply_ambient_background,
    scene_particles,
    scene_filter
)
from prompts import INTRO_PROMPT, END_PROMPT, BADGE_PROMPT
from utils import assign_badge
from streamlit_option_menu import option_menu
from streamlit_custom_notification_box import custom_notification_box
import time
import atexit
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def cleanup_audio():
    """Cleanup function to handle audio resources"""
    if hasattr(st.session_state, 'audio'):
        st.session_state.audio.stop()
    if hasattr(st.session_state, 'narration_progress'):
        st.session_state.narration_progress.stop()

# Register cleanup function
if "cleanup_registered" not in st.session_state:
    atexit.register(cleanup_audio)
    st.session_state.cleanup_registered = True

# Page config
st.set_page_config(
    page_title="Kuku Storyteller",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with enhanced effects
st.markdown("""
<style>
    /* Enhanced button styles */
    .stButton > button {
        width: 100%;
        background-color: rgba(75, 75, 75, 0.2);
        color: inherit;
        padding: 15px 32px;
        border-radius: 12px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
        margin: 5px 0;
        position: relative;
        overflow: hidden;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        border-color: rgba(255, 255, 255, 0.3);
    }
    .stButton > button:active {
        transform: translateY(0px);
    }
    .stButton > button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 5px;
        height: 5px;
        background: rgba(255, 255, 255, 0.5);
        opacity: 0;
        border-radius: 100%;
        transform: scale(1, 1) translate(-50%);
        transform-origin: 50% 50%;
    }
    .stButton > button:focus:not(:active)::after {
        animation: ripple 1s ease-out;
    }
    
    /* Enhanced story text */
    .story-text {
        font-size: 20px;
        line-height: 1.6;
        padding: 20px;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        backdrop-filter: blur(5px);
        border-left: 4px solid rgba(255, 255, 255, 0.2);
        transition: all 0.5s ease-in-out;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { 
            opacity: 0; 
            transform: translateY(10px);
            filter: blur(5px);
        }
        to { 
            opacity: 1; 
            transform: translateY(0);
            filter: blur(0);
        }
    }
    @keyframes ripple {
        0% {
            transform: scale(0, 0);
            opacity: 1;
        }
        20% {
            transform: scale(25, 25);
            opacity: 1;
        }
        100% {
            opacity: 0;
            transform: scale(40, 40);
        }
    }
    
    .fade-in {
        animation: fadeIn 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Enhanced boxes */
    .custom-box {
        animation: fadeIn 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        margin: 10px 0;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
    }
    
    .story-path p {
        margin: 5px 0;
        padding: 10px 15px;
        border-left: 2px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    .story-path p:hover {
        border-left-width: 4px;
        background: rgba(255, 255, 255, 0.05);
    }
    
    /* Progress bar enhancement */
    .stProgress > div > div {
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Sidebar enhancements */
    .sidebar .sidebar-content {
        background: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* API key input styling */
    .api-key-input {
        margin-top: 10px;
        padding: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }
    
    /* Story generation toggle */
    .generation-toggle {
        margin-top: 15px;
        padding: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.kuku = KukuBuddy("stories/thriller.json")
    st.session_state.memory = MemoryManager()
    st.session_state.audio = AudioManager()
    st.session_state.theme_manager = ThemeManager(st.session_state.audio)
    st.session_state.narration_progress = NarrationProgress()
    st.session_state.scene, st.session_state.scene_id = st.session_state.kuku.get_start_scene()
    st.session_state.audio_enabled = True
    st.session_state.theme = "mystery"
    st.session_state.typing_speed = 0.03
    st.session_state.current_mood = "mysterious"
    st.session_state.effects_enabled = True
    st.session_state.start_time = time.time()
    st.session_state.show_achievement = False
    st.session_state._is_running = True
    st.session_state.dynamic_generation = False
    st.session_state.openai_manager = OpenAIManager()

# Prevent unnecessary theme reapplication
if "last_theme" not in st.session_state:
    st.session_state.last_theme = st.session_state.theme

if "last_effects_state" not in st.session_state:
    st.session_state.last_effects_state = st.session_state.effects_enabled

# Apply visual effects only if enabled and if there's a change
if (st.session_state.effects_enabled and 
    (st.session_state.last_theme != st.session_state.theme or 
     st.session_state.last_effects_state != st.session_state.effects_enabled)):
    st.session_state.theme_manager.apply_theme(st.session_state.theme)
    apply_cursor_theme(st.session_state.theme)
    apply_ambient_background(st.session_state.current_mood, 
                           st.session_state.theme_manager.get_theme_colors())
    scene_particles(st.session_state.current_mood)
    scene_filter(st.session_state.current_mood)
    st.session_state.last_theme = st.session_state.theme
    st.session_state.last_effects_state = st.session_state.effects_enabled

# Sidebar with enhanced settings
with st.sidebar:
    st.image("assets/kuku_logo.png", width=100)
    selected = option_menu(
        "Story Settings",
        ["Story", "Settings", "AI Settings", "Progress", "Statistics"],
        icons=["book", "gear", "robot", "graph-up", "trophy"],
        default_index=0,
        styles={
            "nav-link-selected": {"background-color": st.session_state.theme_manager.get_theme_color("primary_color")}
        }
    )
    
    if selected == "Settings":
        # Audio settings with new components
        audio_opts = audio_settings()
        if st.session_state.audio_enabled != audio_opts["enabled"]:
            cleanup_audio()
            st.session_state.audio_enabled = audio_opts["enabled"]
        
        # Visual settings
        st.markdown("---")
        st.markdown("### Visual Settings")
        
        effects_enabled = st.toggle(
            "Enable Visual Effects",
            st.session_state.effects_enabled,
            help="Toggle ambient effects and particles"
        )
        
        theme = st.selectbox(
            "Theme",
            ["mystery", "dark", "light"],
            index=["mystery", "dark", "light"].index(st.session_state.theme)
        )
        
        # Only update if there are actual changes
        if theme != st.session_state.theme or effects_enabled != st.session_state.effects_enabled:
            st.session_state.theme = theme
            st.session_state.effects_enabled = effects_enabled
            st.session_state.theme_manager.apply_theme(theme)
            st.session_state.theme_manager.play_effect("theme_change")
            st.rerun()
            
        st.session_state.typing_speed = st.slider(
            "Text Speed",
            0.01, 0.1, st.session_state.typing_speed,
            help="Adjust how fast the story text appears"
        )
    
    elif selected == "AI Settings":
        st.markdown("### OpenAI Integration")
        
        # API Key input
        st.markdown('<div class="api-key-input">', unsafe_allow_html=True)
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=st.session_state.get("openai_api_key", ""),
            help="Enter your OpenAI API key to enable AI story generation"
        )
        
        if api_key:
            if api_key != st.session_state.get("openai_api_key", ""):
                st.session_state["openai_api_key"] = api_key
                st.session_state.openai_manager.set_api_key(api_key)
                st.success("API key updated!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Dynamic generation toggle
        st.markdown('<div class="generation-toggle">', unsafe_allow_html=True)
        dynamic_generation = st.toggle(
            "Enable AI Story Generation",
            st.session_state.dynamic_generation,
            help="When enabled, the story will dynamically generate new branches based on your choices"
        )
        
        if dynamic_generation != st.session_state.dynamic_generation:
            if dynamic_generation and not api_key:
                st.warning("Please enter an OpenAI API key to enable AI story generation")
                dynamic_generation = False
            else:
                st.session_state.dynamic_generation = dynamic_generation
                if dynamic_generation:
                    st.session_state.kuku.enable_dynamic_generation(st.session_state.openai_manager)
                    st.success("AI story generation enabled!")
                else:
                    st.info("AI story generation disabled")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Model selection
        if st.session_state.dynamic_generation:
            st.selectbox(
                "OpenAI Model",
                ["gpt-3.5-turbo"],
                index=0,
                disabled=True,
                help="Currently only GPT-3.5-turbo is supported"
            )
    
    elif selected == "Progress":
        progress = len(st.session_state.memory.get_path())
        st.progress(min(progress / 5, 1.0), f"Story Progress: {progress} choices made")
        
        if progress > 0:
            st.markdown("""
                <div class='custom-box fade-in'>
                    <h3>Your Journey</h3>
                    <div class='story-path'>
            """, unsafe_allow_html=True)
            
            for scene_id, choice in st.session_state.memory.get_path():
                st.markdown(f"<p>➤ {choice}</p>", unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)

    elif selected == "Statistics":
        st.markdown("### Your Story Journey")
        stats = st.session_state.memory.get_stats()
        
        # Display statistics
        display_story_stats(stats)
        
        st.markdown("### Achievements")
        display_achievements(stats["achievements"])

# Main content area
st.markdown(INTRO_PROMPT, unsafe_allow_html=True)

# Current Scene with enhanced presentation
scene = st.session_state.kuku.get_scene(st.session_state.scene_id)
if scene:
    # Detect scene mood based on content
    def detect_mood(text):
        keywords = {
            "tense": ["sudden", "quickly", "danger", "scared", "rush", "chase", "escape", "hurry"],
            "mysterious": ["strange", "curious", "wonder", "mystery", "unknown", "suspicious", "clue"],
            "peaceful": ["calm", "quiet", "gentle", "safe", "peaceful", "steady", "careful"],
            "dramatic": ["dramatic", "intense", "shocking", "reveal", "twist", "surprise", "discover"]
        }
        
        text = text.lower()
        mood_scores = {mood: sum(1 for word in words if word in text)
                      for mood, words in keywords.items()}
        return max(mood_scores.items(), key=lambda x: x[1])[0] if any(mood_scores.values()) else "mysterious"

    # Update current mood and effects
    new_mood = detect_mood(scene["text"])
    if new_mood != st.session_state.current_mood:
        st.session_state.current_mood = new_mood
        if st.session_state.effects_enabled:
            scene_filter(new_mood)
            apply_ambient_background(new_mood, 
                                  st.session_state.theme_manager.get_theme_color("theme_colors"))
    
    # Show mood indicator if effects are enabled
    if st.session_state.effects_enabled:
        mood_indicator(st.session_state.current_mood, 
                      st.session_state.theme_manager.get_theme_color("theme_colors"))

    with st.container():
        # Get transition animation class
        animation_class = scene_transition("forward")
        
        # Use typing effect with progress tracking
        if "current_text" not in st.session_state:
            st.session_state.current_text = scene["text"]
            text_container = typing_effect(scene["text"], st.session_state.typing_speed)
            
            # Show narration progress if audio is enabled
            if st.session_state.audio_enabled:
                progress_container = st.empty()
                st.session_state.narration_progress.show_progress(
                    len(scene["text"]) * st.session_state.typing_speed,
                    progress_container
                )
        else:
            text_container = st.empty()
            text_container.markdown(
                f'<div class="story-text {animation_class}">{st.session_state.current_text}</div>',
                unsafe_allow_html=True
            )
        
        # Handle audio narration
        if st.session_state.audio_enabled and "last_narrated" not in st.session_state:
            st.session_state.audio.narrate(scene["text"])
            st.session_state.last_narrated = scene["text"]
        
        # Show question with enhanced styling
        if "question" in scene:
            st.markdown(f"<div class='{animation_class}'>", unsafe_allow_html=True)
            custom_notification_box(
                icon='❓',
                textDisplay=scene["question"],
                externalLink='',
                styles={
                    "icon_size": "24px",
                    "background_color": f"{st.session_state.theme_manager.get_theme_color('background_color')}",
                    "border_radius": "10px",
                    "border_left": f"4px solid {st.session_state.theme_manager.get_theme_color('accent_color')}"
                }
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # Show choices with enhanced animations
        if "choices" in scene and scene["choices"]:
            def handle_choice(next_id, choice_text):
                st.session_state.theme_manager.play_effect("button_click")
                cleanup_audio()
                st.session_state.memory.update(st.session_state.scene_id, choice_text)
                
                # If dynamic generation is enabled, potentially generate new content
                if st.session_state.dynamic_generation and next_id == "generate_new":
                    next_id = st.session_state.kuku.generate_choice_scene(
                        st.session_state.scene_id, choice_text
                    )
                
                st.session_state.scene_id = next_id
                st.session_state.last_narrated = None
                st.session_state.current_text = None
                st.rerun()

            # Fix for choice buttons - use a container to ensure proper rendering
            choice_container = st.container()
            with choice_container:
                animated_choice_buttons(scene["choices"], handle_choice)
        else:
            # Enhanced story ending
            story_time = time.time() - st.session_state.start_time
            st.session_state.memory.complete_story(story_time)
            st.session_state.memory.add_mood(st.session_state.current_mood)
            
            st.session_state.theme_manager.play_effect("story_end")
            st.markdown(END_PROMPT, unsafe_allow_html=True)
            
            path = st.session_state.memory.get_path()
            badge = assign_badge(path)
            
            st.session_state.theme_manager.play_effect("badge_earned")
            st.balloons()
            
            # Animated badge reveal with theme-aware colors
            st.markdown(f"""
            <div class='fade-in' style='
                text-align: center;
                padding: 20px;
                background: linear-gradient(135deg, 
                    {st.session_state.theme_manager.get_theme_color('primary_color')}22,
                    {st.session_state.theme_manager.get_theme_color('accent_color')}22
                );
                border-radius: 15px;
                border: 2px solid {st.session_state.theme_manager.get_theme_color('accent_color')}44;
                backdrop-filter: blur(10px);
            '>
                <h2 style='color: {st.session_state.theme_manager.get_theme_color('accent_color')};'>
                    🏅 {badge}
                </h2>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Start New Story", key="restart"):
                st.session_state.start_time = time.time()
                st.session_state.theme_manager.play_effect("button_click")
                cleanup_audio()
                st.session_state.memory.reset()
                st.session_state.current_text = None
                scene, scene_id = st.session_state.kuku.get_start_scene()
                st.session_state.scene_id = scene_id
                st.session_state.last_narrated = None
                st.rerun()
else:
    st.error("Oops! Couldn't load this part of the story.")

st.session_state._is_running = False
