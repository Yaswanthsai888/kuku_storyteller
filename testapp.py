import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import json
from pathlib import Path

# Fix import paths for testing
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules to test
from kuku_buddy import KukuBuddy
from openai_manager import OpenAIManager
from memory_manager import MemoryManager

class TestKukuBuddy(unittest.TestCase):
    """Test the KukuBuddy class functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.story_file = "stories/thriller.json"
        self.kuku = KukuBuddy(self.story_file)
    
    def test_story_loading(self):
        """Test that story loads correctly"""
        self.assertTrue(self.kuku.is_valid())
        self.assertIn("scenes", self.kuku.story)
        self.assertIn("start", self.kuku.story)
    
    def test_get_scene(self):
        """Test getting a scene by ID"""
        scene, scene_id = self.kuku.get_start_scene()
        self.assertIsNotNone(scene)
        self.assertIsNotNone(scene_id)
        self.assertIn("text", scene)
    
    def test_scene_choices(self):
        """Test that scenes have choices"""
        scene, scene_id = self.kuku.get_start_scene()
        self.assertIn("choices", scene)
        self.assertTrue(len(scene["choices"]) >= 2)
    
    @patch('streamlit.session_state', {})
    def test_dynamic_generation_setup(self):
        """Test enabling dynamic generation"""
        openai_manager = OpenAIManager()
        self.kuku.enable_dynamic_generation(openai_manager)
        self.assertTrue(self.kuku.dynamic_generation)
        self.assertEqual(self.kuku.openai_manager, openai_manager)

class TestOpenAIManager(unittest.TestCase):
    """Test the OpenAIManager class functionality"""
    
    @patch('streamlit.session_state', {})
    def setUp(self):
        """Set up test environment"""
        self.openai_manager = OpenAIManager()
    
    def test_initialization(self):
        """Test initialization without API key"""
        self.assertIsNone(self.openai_manager.client)
    
    @patch('openai.OpenAI')
    @patch('streamlit.session_state', {})
    def test_set_api_key(self, mock_openai):
        """Test setting API key"""
        # Mock the OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        # Test setting API key
        result = self.openai_manager.set_api_key("test_api_key")
        self.assertTrue(result)
        self.assertEqual(self.openai_manager.api_key, "test_api_key")
        mock_openai.assert_called_once_with(api_key="test_api_key")
    
    def test_error_scene_creation(self):
        """Test creating error scene"""
        error_scene = self.openai_manager._create_error_scene("Test error")
        self.assertIn("text", error_scene)
        self.assertIn("Test error", error_scene["text"])
        self.assertIn("choices", error_scene)

class TestMemoryManager(unittest.TestCase):
    """Test the MemoryManager class functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.memory = MemoryManager()
    
    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(len(self.memory.path), 0)
        self.assertIn("stories_completed", self.memory.stats)
        self.assertIn("choices_made", self.memory.stats)
    
    def test_update_path(self):
        """Test updating story path"""
        self.memory.update("scene_1", "Test Choice")
        self.assertEqual(len(self.memory.path), 1)
        self.assertEqual(self.memory.path[0], ("scene_1", "Test Choice"))
        self.assertEqual(self.memory.stats["choices_made"], 1)
    
    def test_complete_story(self):
        """Test completing a story"""
        self.memory.complete_story(120)
        self.assertEqual(self.memory.stats["stories_completed"], 1)
        self.assertEqual(self.memory.stats["total_time"], 120)
    
    def test_reset(self):
        """Test resetting memory"""
        self.memory.update("scene_1", "Test Choice")
        self.memory.reset()
        self.assertEqual(len(self.memory.path), 0)

def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestKukuBuddy))
    suite.addTests(loader.loadTestsFromTestCase(TestOpenAIManager))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryManager))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
