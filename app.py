from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import hardware_manager as hw

app = Flask(__name__)
app.secret_key = "your_secret_key_here" 



@app.route("/api/environment")
def get_environment_data():
    """API endpoint to get DHT22 data and a genre recommendation."""
    env_data = hw.get_current_environment()
    
    if env_data:
        temp = env_data["temperature_c"]
        genre = hw.get_music_recommendation_genre(temp)
        
        response = {
            "status": "success",
            "temperature": temp,
            "humidity": env_data["humidity"],
            "recommendation_genre": genre
        }
    else:
        response = {
            "status": "error",
            "message": "Failed to read sensor data. Check DHT22 wiring/resistor."
        }
        
    return jsonify(response)


@app.route("/api/nfc_check")
def nfc_check_uid():
    """API endpoint to check if a card was just scanned."""
    uid = hw.get_last_scanned_uid()
    
    if uid:
        response = {
            "status": "card_detected",
            "uid": uid,
            "message": f"Card {uid} scanned!"
        }
    else:
        response = {
            "status": "waiting",
            "message": "No card detected since last check."
        }
        
    return jsonify(response)



@app.route("/")
def home():
    return render_template("index.html", title="Music4U", stylesheet="style.css")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:
            session['username'] = username
            session['email'] = username
            session['favorite_genre'] = ""
            message = f"Sign In successful! Welcome, {username} 🎵"
        else:
            message = "Please fill out all fields."

    return render_template("signin.html", message=message)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:
            session['username'] = username
            session['email'] = username
            session['favorite_genre'] = ""
            message = f"Sign Up successful! Welcome, {username} 🎵"
        else:
            message = "Please fill out all fields."

    return render_template("signup.html", message=message)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    message = ""
    
    user_data = {
        "username": session.get('username', ''),
        "email": session.get('email', ''),
        "favorite_genre": session.get('favorite_genre', ''),
        "join_date": session.get('join_date', '')
    }
    
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "update":
            username = request.form.get("username")
            email = request.form.get("email")
            favorite_genre = request.form.get("favorite_genre")
            
            if username and email:
                session['username'] = username
                session['email'] = email
                session['favorite_genre'] = favorite_genre
                user_data["username"] = username
                user_data["email"] = email
                user_data["favorite_genre"] = favorite_genre
                message = "Profile updated successfully! 🎵"
            else:
                message = "Please fill out all required fields."
    
    return render_template("profile.html", message=message, user=user_data)


@app.route("/musicplayer")
def player_current():
    return render_template(
        "musicplayer.html",
        song_title="Current Song",
        artist_name="Current Artist",
        album="Sample Album",
        year="2025",
        genre="Electronic",
        lyrics="This song is currently playing.",
        cover_url="/static/cover.png"
    )


playlists = []


@app.route("/playlists")
def playlist_list():
    return render_template("playlists.html", playlists=playlists, title="Playlists")


@app.route("/playlists/create", methods=["GET", "POST"])
def playlist_create():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        if name:
            playlist_id = len(playlists)
            playlists.append({
                "id": playlist_id,
                "name": name,
                "description": description,
                "songs": []
            })
            return redirect(url_for("playlist_list"))
        
    return render_template("playlist_create.html", title="Create Playlist")


@app.route("/playlists/<int:playlist_id>")
def playlist_view(playlist_id):
    playlist = playlists[playlist_id]
    return render_template("playlist_view.html", playlist=playlist)


@app.route("/signout")
def signout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)