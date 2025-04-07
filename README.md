# Kuku Storyteller

An interactive storytelling application built with Streamlit that offers a thrilling choose-your-own-adventure experience.

## Features

- Interactive storytelling with multiple choice paths
- Dynamic story generation using OpenAI integration
- Audio narration with text-to-speech
- Ambient sound effects and music
- Visual themes and mood-based effects
- Achievement system and story statistics
- Responsive design for all devices

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd kuku_storyteller
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Environment Variables

Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Project Structure

- `app.py` - Main application file
- `stories/` - Story content in JSON format
- `assets/` - Static assets (CSS, sounds, images)
- `components/` - Reusable UI components
- Other Python modules for specific functionality

## Contributing

Feel free to submit issues and enhancement requests!