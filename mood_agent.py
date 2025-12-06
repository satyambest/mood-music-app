from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class MoodKeywordAgent:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def generate_keywords(self, text):
        # sentiment analysis using VADER
        sentiment = self.analyzer.polarity_scores(text)
        compound = sentiment['compound']

        # mood label
        if compound >= 0.5:
            mood = "very happy"
        elif compound >= 0.1:
            mood = "happy"
        elif compound > -0.1:
            mood = "neutral"
        elif compound > -0.5:
            mood = "sad"
        else:
            mood = "very sad"

        # energy level (rough)
        energy = "high" if "!" in text or sentiment["pos"] > 0.5 else "low"

        words = text.lower().split()
        topic_words = [w for w in words if len(w) > 4][:5]

        search_keywords = topic_words + [mood] + [energy]

        return {
            "mood_label": mood,
            "energy_level": energy,
            "topic_words": topic_words,
            "search_keywords": search_keywords
        } 