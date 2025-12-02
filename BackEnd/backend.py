from pkgutil import get_data
from flask import session, Flask, render_template

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

def load_song(song_id, db):
    song = db.get_song(song_id)

    session["current_song"] = {
        "title": song.title,
        "artist": song.artist,
        "cover_url": song.cover_url,
        "audio_url": song.audio_url
    }

    return song

@app.route("/play/<int:song_id>")
def play(song_id):
    song = load_song(song_id, db)
    return render_template("musicplayer.html",
        cover_url=song.cover_url,
        song_title=song.title,
        artist_name=song.artist,
        album=song.album,
        year=song.year,
        genre=song.genre,
        lyrics=song.lyrics,
        audio_url=song.audio_url
    )

    return song

@app.route("/profile", methods=["POST"])
def update_profile():
    # pretend we save profile...
    return render_template("profile.html", 
                           message="Profile updated!",
                           user=get_data("user"))

@app.route("/api/history", methods=["POST"])
def add_history():
    data = request.get_json()

    if "history" not in session:
        session["history"] = []

    # Prevent duplicates in a row
    if session["history"] and session["history"][-1]["title"] == data["title"]:
        return {"status": "ignored"}

    session["history"].append(data)

    # Limit to last 20 songs
    session["history"] = session["history"][-20:]

    return {"status": "ok"}
