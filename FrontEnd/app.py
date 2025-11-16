from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key_here"


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


@app.route("/signout")
def signout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
