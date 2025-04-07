# prompts.py

INTRO_PROMPT = """
<div style='text-align: center; padding: 20px;'>
    <h1>Welcome to Kuku Storyteller 🎭</h1>
    <p style='font-size: 1.2em; color: #9e9e9e;'>
        Step into a world where your choices shape the story.
        Every decision leads to a new adventure, every path tells a different tale.
    </p>
    <p style='font-style: italic; color: #7e7e7e;'>
        Choose wisely... or let fate guide your journey.
    </p>
</div>
"""

END_PROMPT = """
<div style='text-align: center; padding: 20px;'>
    <h2>🌟 The End of This Tale... But Not Your Journey 🌟</h2>
    <p style='font-size: 1.1em; color: #9e9e9e;'>
        Your story has reached its conclusion, but many paths remain unexplored.
        Would you like to embark on another adventure?
    </p>
</div>
"""

BADGE_PROMPT = """
<div style='text-align: center; padding: 20px; animation: fadeIn 2s;'>
    <h2 style='color: #ffd700;'>🏅 Achievement Unlocked!</h2>
    <p style='font-size: 1.2em;'>You've earned the badge:</p>
    <h3 style='color: #ffd700; margin: 10px 0;'>{}</h3>
</div>
"""