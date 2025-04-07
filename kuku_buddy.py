# kuku_buddy.py

import json
import random
import logging
import os
from pathlib import Path
from typing import Dict, Tuple, Optional, List
import streamlit as st

class KukuBuddy:
    def __init__(self, story_file):
        self.story = {}
        self.story_file = story_file
        self.openai_manager = None
        self.dynamic_generation = False
        
        try:
            story_path = Path(story_file)
            if not story_path.exists():
                logging.error(f"Story file not found: {story_file}")
                return
                
            with open(story_file, 'r', encoding='utf-8') as f:
                self.story = json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in story file: {e}")
        except Exception as e:
            logging.error(f"Error loading story: {e}")
    
    def enable_dynamic_generation(self, openai_manager) -> None:
        """Enable dynamic story generation with OpenAI"""
        self.openai_manager = openai_manager
        self.dynamic_generation = True
        logging.info("Dynamic story generation enabled")

    def get_scene(self, scene_id):
        """Get a scene by ID with error handling"""
        try:
            if not self.story or "scenes" not in self.story:
                logging.error("Story not properly loaded")
                return None
                
            return self.story["scenes"].get(scene_id, None)
        except Exception as e:
            logging.error(f"Error getting scene {scene_id}: {e}")
            return None

    def get_next_scene(self, current_scene_id, user_choice):
        """Get next scene based on user choice with validation"""
        try:
            scene = self.get_scene(current_scene_id)
            if not scene:
                logging.error(f"Invalid current scene: {current_scene_id}")
                return None, None

            choices = scene.get("choices", {})
            next_scene_id = choices.get(user_choice)

            if not next_scene_id:
                logging.error(f"Invalid choice: {user_choice}")
                return None, None
            
            # Check if we need to dynamically generate this scene
            if self.dynamic_generation and self.openai_manager and next_scene_id.endswith("_ai"):
                # Scene doesn't exist yet, generate it
                if next_scene_id not in self.story["scenes"]:
                    story_context = self._build_story_context(current_scene_id)
                    next_scene_id, self.story = self.openai_manager.extend_story(
                        self.story, current_scene_id, user_choice
                    )
                    # Save the updated story
                    self._save_story()

            next_scene = self.get_scene(next_scene_id)
            if not next_scene:
                logging.error(f"Invalid next scene: {next_scene_id}")
                return None, None
                
            return next_scene_id, next_scene
        except Exception as e:
            logging.error(f"Error getting next scene: {e}")
            return None, None

    def get_start_scene(self):
        """Get starting scene with fallback"""
        try:
            if not self.story:
                logging.error("Story not loaded")
                return None, None
                
            start_id = self.story.get("start")
            if not start_id:
                # Fallback to first scene if start not specified
                if "scenes" in self.story and self.story["scenes"]:
                    start_id = next(iter(self.story["scenes"].keys()))
                else:
                    logging.error("No scenes found in story")
                    return None, None
                    
            scene = self.get_scene(start_id)
            return scene, start_id
        except Exception as e:
            logging.error(f"Error getting start scene: {e}")
            return None, None
    
    def generate_choice_scene(self, current_scene_id: str, choice_text: str) -> str:
        """Generate a new scene based on user choice"""
        if not self.dynamic_generation or not self.openai_manager:
            logging.error("Dynamic generation not enabled")
            return current_scene_id
        
        try:
            # Generate a unique ID for the new scene
            new_scene_id = f"{current_scene_id}_choice_{len(self.story['scenes']) + 1}"
            
            # Build context for generation
            story_context = self._build_story_context(current_scene_id)
            
            # Generate new scene and update story
            new_scene_id, self.story = self.openai_manager.extend_story(
                self.story, current_scene_id, choice_text
            )
            
            # Save the updated story
            self._save_story()
            
            return new_scene_id
        except Exception as e:
            logging.error(f"Error generating choice scene: {e}")
            return current_scene_id
    
    def _build_story_context(self, current_scene_id: str) -> Dict:
        """Build context for story generation"""
        # Get the current scene and its ancestors
        current_scene = self.get_scene(current_scene_id)
        
        # Build context with story metadata and relevant scenes
        context = {
            "title": self.story.get("title", "Interactive Story"),
            "genre": self.story.get("genre", "Thriller"),
            "previous_scenes": []
        }
        
        # Add current scene to context
        if current_scene:
            context["previous_scenes"].append({
                "id": current_scene_id,
                "text": current_scene.get("text", ""),
                "question": current_scene.get("question", ""),
                "choices": current_scene.get("choices", {})
            })
        
        return context
    
    def _save_story(self) -> None:
        """Save the current story to file"""
        try:
            with open(self.story_file, 'w', encoding='utf-8') as f:
                json.dump(self.story, f, indent=2)
            logging.info(f"Story saved to {self.story_file}")
        except Exception as e:
            logging.error(f"Error saving story: {e}")

    def is_valid(self):
        """Check if story is properly loaded"""
        return bool(self.story and "scenes" in self.story and self.story["scenes"])
