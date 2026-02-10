import os
import json
from groq import Groq

GROQ_MODEL = "llama-3.3-70b-versatile"
class MoodKeywordAgent:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
        if not self.client.api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")

    def generate_keywords(self, text):
        # Create a prompt for mood analysis
        prompt = f"""
Analyze the following text and determine the user's mood and emotional state.
Return a JSON object with the following structure:
{{
    "mood_label": "one of: very happy, happy, neutral, sad, very sad, excited, anxious, calm, angry, frustrated",
    "energy_level": "high or low",
    "confidence": "a number between 0 and 1 indicating confidence in the analysis",
    "emotions": ["list", "of", "detected", "emotions"],
    "example_songs": ["list", "of", "example", "songs", "matching", "the", "mood"],
    "spotify_search_keywords": ["list", "of", "keywords", "to", "search", "on", "Spotify"],
    "search_full_text":"FUll TExt to search in spotify"
}}
Example input: "I just got a promotion at work and I'm feeling great!"
Example output: {{
    "mood_label": "very happy",
    "energy_level": "high",
    "confidence": 0.95,
    "emotions": ["joy", "excitement"],
    "example_songs": ["Happy - Pharrell Williams", "Good Vibrations - The Beach Boys"],
    "spotify_search_keywords": ["happy", "upbeat", "celebration"],
    "search_full_text": "celebration songs"
}}

Text to analyze: "{text}"

Return only the JSON object, no additional text.
"""

        try:
            response = self.client.chat.completions.create(
                model=GROQ_MODEL,  # Using Llama 3 70B Versatile model
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )

            result_text = response.choices[0].message.content.strip()

            # Try to parse the JSON response
            try:
                mood_data = json.loads(result_text)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return self.generate_keywords(text)

            # Extract topic words from the text
            words = text.lower().split()
            topic_words = [w for w in words if len(w) > 4][:5]

            # Create search keywords
            search_keywords = topic_words + [mood_data.get("mood_label", "neutral")]

            return {
                "mood_label": mood_data.get("mood_label", "neutral"),
                "energy_level": mood_data.get("energy_level", "medium"),
                "topic_words": topic_words,
                "search_keywords": search_keywords,
                "confidence": mood_data.get("confidence", 0.5),
                "example_songs": mood_data.get("example_songs", []),
                "spotify_search_keywords": mood_data.get("spotify_search_keywords", []),
                "emotions": mood_data.get("emotions", ["neutral"])
            }

        except Exception as e:
            print(f"Error calling Groq API: {e}")
            # Fallback to basic analysis
            return {
                "mood_label": "neutral",
                "energy_level": "medium",
                "topic_words": [],
                "search_keywords": ["neutral"],
                "confidence": 0.0,
                "emotions": ["neutral"]
            } 