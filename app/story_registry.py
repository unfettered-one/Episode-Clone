from configuration import settings

base_url = settings.get_base_url()
stories = {
    "mystery_mansion": {
        "id": "mystery_mansion",
        "title": "Mystery at the Old Mansion",
        "description": """You are a renowned but jaded detective, summoned to the remote and fog-shrouded Blackwood Manor. Its owner, the eccentric billionaire Alistair Blackwood, has vanished without a trace. The family calls it a simple missing person case, but the locals whisper of a century-old curse and a ghostly bride who roams the decaying halls.

Inside, you'll find a labyrinth of secret passages, cryptic puzzles, and a cast of suspicious family members, each with a motive hidden behind a veneer of grief. Unravel a dark history of forbidden love, betrayal, and madness. Is a vengeful spirit truly haunting the estate, or is a flesh-and-blood monster hiding in plain sight? Every clue you uncover and every choice you make will pull you deeper into the mansion's chilling heart. Solve the mystery before you become its next permanent resident.""",
        "story_path": "./app/story_docs/mystery_mansion",
        "cover_image": f"{base_url}/assets/story-mystery.jpg",
        "genre": "Mystery",
    },
    "space_rebellion": {
        "id": "space_rebellion",
        "title": "The Space Rebellion",
        "description": "You are the leader of a rebellion on Mars, navigating political chaos.",
        "story_path": "./app/story_docs/space_rebellion",
        "cover_image": f"{base_url}/assets/story-drama.jpg",
        "genre": "Sci-Fi",
    },
}
