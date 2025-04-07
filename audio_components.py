import streamlit as st
import threading
import time

class NarrationProgress:
    def __init__(self):
        self._progress = 0
        self._lock = threading.Lock()
        self._stop = False
        self._thread = None

    def reset(self):
        """Reset progress tracking"""
        with self._lock:
            self._progress = 0
            self._stop = False

    def stop(self):
        """Stop progress tracking"""
        with self._lock:
            self._stop = True
            if self._thread and self._thread.is_alive():
                self._thread.join(timeout=1.0)

    def show_progress(self, duration, container):
        """Show animated progress bar for narration"""
        self.reset()
        step = 100 / (duration * 10)  # Update 10 times per second

        def update_progress():
            try:
                while self._progress < 100 and not self._stop:
                    with self._lock:
                        self._progress = min(100, self._progress + step)
                    
                    container.markdown(
                        f"""<div class="narration-progress">
                            📢 Narrating... {int(self._progress)}%
                        </div>""",
                        unsafe_allow_html=True
                    )
                    
                    if self._progress >= 100:
                        break
                        
                    time.sleep(0.1)
                
                if not self._stop:
                    container.empty()
            except Exception as e:
                print(f"Error updating progress: {e}")
            finally:
                with self._lock:
                    self._thread = None

        # Start progress updates in a separate thread
        self._thread = threading.Thread(target=update_progress)
        self._thread.daemon = True
        self._thread.start()

def audio_settings():
    """Enhanced audio settings with visual feedback"""
    st.markdown("""
        <style>
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .setting-group {
                animation: fadeIn 0.5s ease-out;
                padding: 15px;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.05);
                margin: 10px 0;
                backdrop-filter: blur(5px);
            }
            .setting-group:hover {
                background: rgba(255, 255, 255, 0.08);
            }
            .volume-indicator {
                height: 20px;
                background: linear-gradient(90deg, #4CAF50, #81C784);
                border-radius: 10px;
                transition: width 0.3s ease;
            }
        </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="setting-group">', unsafe_allow_html=True)
        enabled = st.toggle("Enable Audio", value=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="setting-group">', unsafe_allow_html=True)
        speed = st.select_slider(
            "Narration Speed",
            options=["Slow", "Normal", "Fast"],
            value="Normal"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="setting-group">', unsafe_allow_html=True)
        volume = st.slider(
            "Volume",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Adjust the volume of narration and sound effects"
        )
        
        # Visual volume indicator
        st.markdown(f"""
            <div style="width: 100%; height: 20px; background: rgba(255, 255, 255, 0.1); border-radius: 10px; overflow: hidden;">
                <div class="volume-indicator" style="width: {volume * 100}%;"></div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        return {
            "enabled": enabled,
            "speed": speed,
            "volume": volume
        }