from flask import Flask, render_template, request

app = Flask(__name__)


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
            message = f"Sign Up successful! Welcome, {username} 🎵"
        else:
            message = "Please fill out all fields."

    return render_template("signup.html", message=message)



if __name__ == "__main__":
    app.run(debug=True)
