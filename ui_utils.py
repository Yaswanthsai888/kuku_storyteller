import streamlit as st
import os
from pathlib import Path

# Load custom CSS
def load_custom_css():
    css_path = Path(__file__).parent / "assets" / "custom.css"
    if css_path.exists():
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"Custom CSS file not found at {css_path}")

# Update app.py to load custom CSS
def update_app_with_css():
    app_path = Path(__file__).parent / "app.py"
    if not app_path.exists():
        return False
    
    with open(app_path, "r") as f:
        content = f.read()
    
    # Check if custom CSS is already imported
    if "load_custom_css()" in content:
        return True
    
    # Add import statement
    if "from utils import assign_badge" in content:
        content = content.replace(
            "from utils import assign_badge",
            "from utils import assign_badge\nfrom ui_utils import load_custom_css"
        )
    
    # Add CSS loading after page config
    if "st.set_page_config(" in content:
        content = content.replace(
            ")\n",
            ")\n\n# Load custom CSS\nload_custom_css()\n",
            1  # Replace only the first occurrence
        )
    
    # Write updated content
    with open(app_path, "w") as f:
        f.write(content)
    
    return True

if __name__ == "__main__":
    # This allows testing this module directly
    st.title("UI Utilities Test")
    load_custom_css()
    st.write("Custom CSS loaded successfully!")
