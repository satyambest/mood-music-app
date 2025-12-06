from flask import Flask, render_template, request
from mood_agent import MoodKeywordAgent
import urllib.parse

app = Flask(__name__)
agent = MoodKeywordAgent()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        essay = request.form.get("essay", "")

        if not essay.strip():
            return render_template("index.html", error="Please write something 😊")

        analysis = agent.generate_keywords(essay)
        keywords = analysis["search_keywords"][:8]
        query = " ".join(keywords)

        # simple Spotify search link
        spotify_url = "https://open.spotify.com/search/" + urllib.parse.quote(query)

        return render_template(
            "index.html",
            essay=essay,
            analysis=analysis,
            query=query,
            spotify_url=spotify_url
        )

    # first time: just show empty page
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True) 