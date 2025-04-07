# runner.py

from kuku_buddy import KukuBuddy

def run_cli_story():
    kuku = KukuBuddy("stories/thriller.json")
    scene, current_id = kuku.get_start_scene()

    while True:
        scene = kuku.get_scene(current_id)
        if not scene:
            print("The story ends here.")
            break

        print(f"\n{scene['text']}\n")
        choices = scene.get("choices", {})
        if not choices:
            print("🎉 The End!")
            break

        for i, choice in enumerate(choices.keys(), 1):
            print(f"{i}. {choice}")

        choice_idx = input("\nEnter choice number: ")
        try:
            choice_text = list(choices.keys())[int(choice_idx) - 1]
            current_id, _ = kuku.get_next_scene(current_id, choice_text)
        except:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    run_cli_story()
