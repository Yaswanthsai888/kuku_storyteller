import streamlit as st
import time
from typing import Dict, Callable

def typing_effect(text: str, speed: float = 0.03):
    """Display text with a typing animation effect"""
    container = st.empty()
    displayed_text = ""
    
    # Process special markdown characters
    text = text.replace("*", "\\*").replace("_", "\\_")
    
    for char in text:
        displayed_text += char
        container.markdown(
            f'<div class="story-text fade-in">{displayed_text}▌</div>', 
            unsafe_allow_html=True
        )
        time.sleep(speed)
    
    # Final display without cursor
    container.markdown(
        f'<div class="story-text fade-in">{displayed_text}</div>',
        unsafe_allow_html=True
    )
    return container

def animated_choice_buttons(choices: Dict[str, str], on_click: Callable):
    """Display choice buttons with animation and hover effects"""
    # Fix: Use a more reliable layout for buttons
    # Instead of using columns which can cause rendering issues,
    # stack buttons vertically for better reliability
    
    st.markdown("""
        <style>
            .choice-button {
                width: 100%;
                position: relative;
                overflow: hidden;
                margin-bottom: 10px;
            }
            
            .choice-button::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(
                    90deg,
                    transparent,
                    rgba(255, 255, 255, 0.2),
                    transparent
                );
                transition: 0.5s;
            }
            
            .choice-button:hover::before {
                left: 100%;
            }
            
            /* Enhanced button styles for better visibility */
            .stButton > button {
                margin-bottom: 12px !important;
                min-height: 60px !important;
                font-size: 16px !important;
                font-weight: 500 !important;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
                transition: transform 0.2s ease, box-shadow 0.2s ease !important;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
            }
            
            .stButton > button:active {
                transform: translateY(1px) !important;
                box-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Create a container for all buttons
    button_container = st.container()
    
    # Track if any button was clicked
    button_clicked = False
    
    # Display each choice as a button
    with button_container:
        for idx, (choice_text, next_id) in enumerate(choices.items()):
            # Use a unique key for each button based on both index and text
            # This helps prevent key collisions that can cause button issues
            button_key = f"choice_{idx}_{hash(choice_text) % 10000}"
            
            if st.button(
                choice_text,
                key=button_key,
                use_container_width=True,
                help="Click to choose this path"
            ):
                button_clicked = True
                on_click(next_id, choice_text)
                return True
    
    return button_clicked
