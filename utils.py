# utils.py

def assign_badge(path):
    """
    Assigns a badge based on the choices made in the story path.
    The path is a list of (scene_id, choice_text) tuples.
    """
    if not path:
        return "Mystery Novice"

    investigative_keywords = ["search", "investigate", "check", "question", "follow", "observe"]
    action_keywords = ["chase", "confront", "alert", "join"]

    investigative_count = sum(1 for _, choice in path if any(word in choice.lower() for word in investigative_keywords))
    action_count = sum(1 for _, choice in path if any(word in choice.lower() for word in action_keywords))

    if investigative_count > action_count:
        return "Master Detective"
    elif action_count > investigative_count:
        return "Dynamic Sleuth"
    elif len(path) >= 4:  # Player reached a conclusion
        return "Case Solver"
    else:
        return "Amateur Investigator"
