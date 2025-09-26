from configuration import settings

base_url = settings.get_base_url()
stories = {
    "mystery_mansion": {
        "id": "mystery_mansion",
        "title": "Mystery at the Old Mansion",
        "description": "A detective investigates a haunted mansion full of secrets.",
        "story_path": "./app/story_docs/mystery_mansion",
        "cover_image": f"{base_url}/assets/story-mystery.jpg",
    },
    "space_rebellion": {
        "id": "space_rebellion",
        "title": "The Space Rebellion",
        "description": "You are the leader of a rebellion on Mars, navigating political chaos.",
        "story_path": f"{base_url}/assets/story-drama.jpg",
    },
}
