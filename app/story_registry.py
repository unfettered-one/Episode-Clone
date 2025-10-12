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
    "aligning_the_stars": {
        "id": "aligning_the_stars",
        "title": "Aligning The Stars",
        "description": "When your hot, mysterious celebrity invites you to a charity gala, you are determined to be reunited. Will the stars align for you to find each other? \n \nYour life takes an unexpected turn when you cross paths with Adrian Vega, a mysterious rising celebrity who seems to see something in you that no one else does. Just as you’re ready to forget the fleeting moment, a surprise invitation arrives: Adrian wants you at a glittering charity gala—an event filled with glamour, secrets, and watchful eyes.The spotlight is dazzling, but dangerous. Will you dare to chase this spark with Adrian, or will the world of fame tear you apart before your story can begin?",
        "story_path": "./app/story_docs/aligning_the_stars",
        "cover_image": f"{base_url}/assets/story-romance.jpg",
        "genre": "Romance",
    },
}
