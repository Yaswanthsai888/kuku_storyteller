import os
import json
import logging
import openai
import streamlit as st
from typing import Dict, List, Tuple, Optional

class OpenAIManager:
    """Manages interactions with OpenAI API for story generation"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI client with API key"""
        self.api_key = api_key
        self.client = None
        self.system_prompt = """
        You are an expert storyteller specializing in thriller narratives. 
        Your task is to continue an interactive story based on the user's choices.
        
        Guidelines:
        - Create engaging, suspenseful content with vivid descriptions
        - Keep responses concise (100-150 words per scene)
        - Include subtle clues and foreshadowing
        - Maintain consistent tone and characters
        - End each scene with a clear question and 2-3 distinct choices
        - Each choice should lead to meaningfully different outcomes
        """
        self.initialize_client()
    
    def initialize_client(self) -> None:
        """Initialize OpenAI client with API key"""
        try:
            # Try to get API key from environment or session state
            api_key = self.api_key or st.session_state.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
            
            if api_key:
                self.client = openai.OpenAI(api_key=api_key)
                logging.info("OpenAI client initialized successfully")
            else:
                logging.warning("No OpenAI API key provided")
        except Exception as e:
            logging.error(f"Error initializing OpenAI client: {e}")
    
    def set_api_key(self, api_key: str) -> bool:
        """Set or update API key"""
        try:
            self.api_key = api_key
            st.session_state["openai_api_key"] = api_key
            self.initialize_client()
            return True
        except Exception as e:
            logging.error(f"Error setting API key: {e}")
            return False
    
    def generate_scene(self, story_context: Dict, current_scene_id: str, 
                      user_choice: Optional[str] = None) -> Dict:
        """Generate a new scene based on story context and user choice"""
        if not self.client:
            logging.error("OpenAI client not initialized")
            return self._create_error_scene("API connection error. Please check your API key.")
        
        try:
            # Build prompt with story context
            prompt = self._build_prompt(story_context, current_scene_id, user_choice)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            # Parse response into scene format
            scene_text = response.choices[0].message.content
            return self._parse_scene_text(scene_text, current_scene_id)
            
        except Exception as e:
            logging.error(f"Error generating scene: {e}")
            return self._create_error_scene(f"Story generation error: {str(e)}")
    
    def generate_choices(self, story_context: Dict, current_scene_id: str, 
                        scene_text: str) -> Dict[str, str]:
        """Generate choices for a scene"""
        if not self.client:
            logging.error("OpenAI client not initialized")
            return {"Try again": current_scene_id}
        
        try:
            # Build prompt for choices
            prompt = f"""
            Based on this scene in our thriller story:
            
            {scene_text}
            
            Generate 2-3 interesting choices for the reader. Each choice should lead to a different direction.
            Format your response as a JSON object with choice text as keys and placeholder IDs as values.
            Example: {{"Investigate the basement": "next_scene_1", "Call for backup": "next_scene_2"}}
            """
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You generate choices for interactive stories in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            # Parse response into choices format
            choices_text = response.choices[0].message.content
            return self._parse_choices_text(choices_text, current_scene_id)
            
        except Exception as e:
            logging.error(f"Error generating choices: {e}")
            return {"Try again": current_scene_id}
    
    def extend_story(self, story_data: Dict, current_scene_id: str, 
                    user_choice: str) -> Tuple[str, Dict]:
        """Generate a new scene and add it to the story"""
        if not self.client:
            logging.error("OpenAI client not initialized")
            return current_scene_id, story_data
        
        try:
            # Generate a unique ID for the new scene
            new_scene_id = f"scene_{len(story_data['scenes']) + 1}_ai"
            
            # Get the current scene
            current_scene = story_data["scenes"].get(current_scene_id, {})
            
            # Build context for generation
            story_context = {
                "title": story_data.get("title", "Thriller Story"),
                "genre": story_data.get("genre", "Thriller"),
                "previous_scenes": [
                    {"id": scene_id, "text": scene.get("text", ""), "choices": scene.get("choices", {})}
                    for scene_id, scene in story_data["scenes"].items()
                    if scene_id == current_scene_id or scene_id in current_scene.get("choices", {}).values()
                ]
            }
            
            # Generate new scene
            new_scene = self.generate_scene(story_context, current_scene_id, user_choice)
            
            # Add the new scene to the story
            story_data["scenes"][new_scene_id] = new_scene
            
            # Update the current scene's choices to point to the new scene
            if current_scene and "choices" in current_scene:
                current_scene["choices"][user_choice] = new_scene_id
            
            return new_scene_id, story_data
            
        except Exception as e:
            logging.error(f"Error extending story: {e}")
            return current_scene_id, story_data
    
    def _build_prompt(self, story_context: Dict, current_scene_id: str, 
                     user_choice: Optional[str] = None) -> str:
        """Build prompt for scene generation"""
        title = story_context.get("title", "Thriller Story")
        genre = story_context.get("genre", "Thriller")
        
        prompt = f"""
        You're continuing a {genre} story titled "{title}".
        
        """
        
        if user_choice:
            prompt += f"The reader chose: \"{user_choice}\"\n\n"
        
        # Add previous scenes for context
        previous_scenes = story_context.get("previous_scenes", [])
        if previous_scenes:
            prompt += "Previous scenes:\n"
            for scene in previous_scenes:
                prompt += f"- {scene.get('text', '')}\n"
        
        prompt += """
        Generate the next scene in this thriller story. Include:
        1. Vivid description (100-150 words)
        2. A question for the reader
        3. 2-3 possible choices
        
        Format your response like this:
        [SCENE]
        Your scene text here...
        [QUESTION]
        Your question here...
        [CHOICES]
        Choice 1
        Choice 2
        (Choice 3 - optional)
        """
        
        return prompt
    
    def _parse_scene_text(self, scene_text: str, current_scene_id: str) -> Dict:
        """Parse generated text into scene format"""
        try:
            # Extract sections
            scene_parts = {}
            current_section = None
            
            for line in scene_text.split('\n'):
                line = line.strip()
                if line in ['[SCENE]', '[QUESTION]', '[CHOICES]']:
                    current_section = line
                    scene_parts[current_section] = []
                elif current_section and line:
                    scene_parts[current_section].append(line)
            
            # Build scene object
            scene = {
                "text": ' '.join(scene_parts.get('[SCENE]', ['Scene text missing'])),
                "question": ' '.join(scene_parts.get('[QUESTION]', ['What do you do next?']))
            }
            
            # Add choices
            choices = scene_parts.get('[CHOICES]', [])
            if choices:
                choice_dict = {}
                for i, choice in enumerate(choices):
                    next_scene_id = f"{current_scene_id}_choice_{i+1}"
                    choice_dict[choice] = next_scene_id
                scene["choices"] = choice_dict
            
            return scene
            
        except Exception as e:
            logging.error(f"Error parsing scene text: {e}")
            return self._create_error_scene("Error processing the story. Please try again.")
    
    def _parse_choices_text(self, choices_text: str, current_scene_id: str) -> Dict[str, str]:
        """Parse generated choices text into choices format"""
        try:
            # Extract JSON from the response
            choices_text = choices_text.strip()
            
            # Find JSON object in the text
            start_idx = choices_text.find('{')
            end_idx = choices_text.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = choices_text[start_idx:end_idx]
                choices = json.loads(json_str)
                return choices
            
            # Fallback: parse line by line if JSON not found
            choices = {}
            for i, line in enumerate(choices_text.split('\n')):
                line = line.strip()
                if line and not line.startswith('{') and not line.startswith('}'):
                    next_scene_id = f"{current_scene_id}_choice_{i+1}"
                    choices[line] = next_scene_id
            
            return choices if choices else {"Continue": f"{current_scene_id}_continue"}
            
        except Exception as e:
            logging.error(f"Error parsing choices text: {e}")
            return {"Try again": current_scene_id}
    
    def _create_error_scene(self, error_message: str) -> Dict:
        """Create an error scene when generation fails"""
        return {
            "text": f"Story generation paused. {error_message}",
            "question": "Would you like to try again?",
            "choices": {
                "Try again": "retry",
                "Start over": "start"
            }
        }
