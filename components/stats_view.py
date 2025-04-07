import streamlit as st

def display_achievements(achievements):
    """Display achievements with progress bars"""
    st.markdown("""
        <style>
            .achievement {
                background: rgba(255, 255, 255, 0.05);
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                border-left: 4px solid gold;
                backdrop-filter: blur(5px);
            }
            .achievement-progress {
                margin-top: 5px;
                height: 6px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 3px;
                overflow: hidden;
            }
            .progress-bar {
                height: 100%;
                background: linear-gradient(90deg, #FFD700, #FFA500);
                transition: width 0.5s ease-in-out;
            }
        </style>
    """, unsafe_allow_html=True)

    for achievement in achievements:
        progress = (achievement["progress"] / achievement["target"]) * 100
        st.markdown(f"""
            <div class="achievement">
                <h4>{achievement["name"]}</h4>
                <p>{achievement["description"]}</p>
                <div class="achievement-progress">
                    <div class="progress-bar" style="width: {progress}%;"></div>
                </div>
                <small>{achievement["progress"]}/{achievement["target"]}</small>
            </div>
        """, unsafe_allow_html=True)

def display_story_stats(stats):
    """Display story statistics with animations"""
    st.markdown("""
        <style>
            @keyframes countUp {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .stat-card {
                animation: countUp 0.5s ease-out forwards;
                background: rgba(255, 255, 255, 0.05);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin: 10px 0;
                backdrop-filter: blur(5px);
            }
            .stat-value {
                font-size: 24px;
                font-weight: bold;
                margin: 10px 0;
            }
            .stat-label {
                font-size: 14px;
                opacity: 0.8;
            }
        </style>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    
    with cols[0]:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{stats['stories_completed']}</div>
                <div class="stat-label">Stories Completed</div>
            </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{stats['choices_made']}</div>
                <div class="stat-label">Choices Made</div>
            </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        avg_time = int(stats['avg_time_per_story'])
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{avg_time}s</div>
                <div class="stat-label">Avg. Time per Story</div>
            </div>
        """, unsafe_allow_html=True)

    # Mood tracking
    st.markdown("### Moods Experienced")
    mood_cols = st.columns(4)
    all_moods = ["mysterious", "tense", "peaceful", "dramatic"]
    
    for idx, mood in enumerate(all_moods):
        with mood_cols[idx]:
            is_experienced = mood in stats['moods_experienced']
            st.markdown(f"""
                <div class="stat-card" style="
                    border: 2px solid {'gold' if is_experienced else 'rgba(255,255,255,0.1)'};
                    opacity: {1 if is_experienced else 0.5};
                ">
                    <div class="stat-value">{'✨' if is_experienced else '🔒'}</div>
                    <div class="stat-label">{mood.title()}</div>
                </div>
            """, unsafe_allow_html=True)