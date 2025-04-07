# memory_manager.py

import time
from typing import List, Dict, Set, Tuple

class MemoryManager:
    def __init__(self):
        self.path = []
        self.stats = {
            "stories_completed": 0,
            "choices_made": 0,
            "badges_earned": set(),
            "moods_experienced": set(),
            "total_time": 0,
            "fastest_completion": float('inf'),
            "favorite_choices": {},
            "mood_transitions": []
        }
        self.achievements = {
            "Explorer": {
                "description": "Made 10 different choices",
                "unlocked": False,
                "progress": 0,
                "target": 10,
                "icon": "🗺️"
            },
            "Speed Reader": {
                "description": "Complete a story in under 2 minutes",
                "unlocked": False,
                "progress": 0,
                "target": 1,
                "icon": "⚡"
            },
            "Story Weaver": {
                "description": "Experience all story moods",
                "unlocked": False,
                "progress": 0,
                "target": 4,
                "icon": "🎭"
            },
            "Mood Master": {
                "description": "Experience 3 different moods in one story",
                "unlocked": False,
                "progress": 0,
                "target": 3,
                "icon": "🎪"
            },
            "Detective": {
                "description": "Choose investigative options 5 times",
                "unlocked": False,
                "progress": 0,
                "target": 5,
                "icon": "🔍"
            }
        }
        self.start_time = time.time()

    def update(self, scene_id: str, choice: str) -> None:
        """Update story path and stats"""
        self.path.append((scene_id, choice))
        self.stats["choices_made"] += 1
        
        # Track favorite choices
        self.stats["favorite_choices"][choice] = self.stats["favorite_choices"].get(choice, 0) + 1
        
        # Check for investigative choices
        investigative_keywords = ["investigate", "search", "examine", "look", "study", "analyze"]
        if any(keyword in choice.lower() for keyword in investigative_keywords):
            self.achievements["Detective"]["progress"] += 1
        
        self._check_achievements()

    def add_mood(self, mood: str) -> None:
        """Track experienced moods"""
        self.stats["moods_experienced"].add(mood)
        self.stats["mood_transitions"].append((time.time() - self.start_time, mood))
        
        # Check for mood-related achievements
        if len(self.stats["moods_experienced"]) >= 4:
            self._unlock_achievement("Story Weaver")
        
        # Check for mood variety in current story
        story_moods = set(mood for _, mood in self.stats["mood_transitions"])
        if len(story_moods) >= 3:
            self._unlock_achievement("Mood Master")

    def complete_story(self, time_taken: float) -> None:
        """Record story completion"""
        self.stats["stories_completed"] += 1
        self.stats["total_time"] += time_taken
        
        # Track fastest completion
        if time_taken < self.stats["fastest_completion"]:
            self.stats["fastest_completion"] = time_taken
        
        if time_taken < 120:  # 2 minutes
            self._unlock_achievement("Speed Reader")

    def get_path(self) -> List[Tuple[str, str]]:
        """Get current story path"""
        return self.path

    def get_stats(self) -> Dict:
        """Get current statistics with analysis"""
        unique_choices = len(set(choice for _, choice in self.path))
        story_length = len(self.path)
        
        return {
            **self.stats,
            "unique_choices": unique_choices,
            "story_length": story_length,
            "avg_time_per_story": (
                self.stats["total_time"] / self.stats["stories_completed"]
                if self.stats["stories_completed"] > 0 else 0
            ),
            "choice_variety": unique_choices / story_length if story_length > 0 else 0,
            "achievements": self._get_unlocked_achievements(),
            "favorite_mood": self._get_favorite_mood(),
            "playstyle": self._analyze_playstyle()
        }

    def _check_achievements(self) -> None:
        """Check and update achievements"""
        unique_choices = len(set(choice for _, choice in self.path))
        self.achievements["Explorer"]["progress"] = unique_choices
        
        if unique_choices >= 10:
            self._unlock_achievement("Explorer")
        
        if self.achievements["Detective"]["progress"] >= 5:
            self._unlock_achievement("Detective")

    def _unlock_achievement(self, achievement_name: str) -> None:
        """Unlock an achievement and add it to earned badges"""
        if achievement_name in self.achievements and not self.achievements[achievement_name]["unlocked"]:
            self.achievements[achievement_name]["unlocked"] = True
            self.achievements[achievement_name]["progress"] = self.achievements[achievement_name]["target"]
            self.stats["badges_earned"].add(achievement_name)

    def _get_unlocked_achievements(self) -> List[Dict]:
        """Get list of unlocked achievements with details"""
        return [
            {
                "name": name,
                "description": data["description"],
                "progress": data["progress"],
                "target": data["target"],
                "icon": data["icon"]
            }
            for name, data in self.achievements.items()
            if data["unlocked"]
        ]

    def _get_favorite_mood(self) -> str:
        """Determine the most experienced mood"""
        if not self.stats["mood_transitions"]:
            return "mysterious"
        
        mood_counts = {}
        for _, mood in self.stats["mood_transitions"]:
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        return max(mood_counts.items(), key=lambda x: x[1])[0]

    def _analyze_playstyle(self) -> str:
        """Analyze player's story choices to determine playstyle"""
        if not self.path:
            return "Newcomer"
        
        # Count choice types
        investigative = sum(1 for _, choice in self.path if any(word in choice.lower() for word in ["investigate", "search", "examine"]))
        action = sum(1 for _, choice in self.path if any(word in choice.lower() for word in ["chase", "run", "fight", "escape"]))
        careful = sum(1 for _, choice in self.path if any(word in choice.lower() for word in ["wait", "observe", "think", "plan"]))
        
        # Determine primary playstyle
        styles = {
            "Detective": investigative,
            "Action Seeker": action,
            "Strategic Thinker": careful
        }
        
        return max(styles.items(), key=lambda x: x[1])[0] if any(styles.values()) else "Balanced Explorer"

    def reset(self) -> None:
        """Reset current story path but keep overall stats"""
        self.path = []
        self.start_time = time.time()
        self.stats["mood_transitions"] = []
