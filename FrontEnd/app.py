from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", title="Music4U", stylesheet="style.css")


@app.route("/auth", methods=["GET", "POST"])
def auth():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        form_type = request.form.get("form_type")

        if username and password:
            message = f"{form_type} successful! Welcome, {username} 🎵"
        else:
            message = "Please fill out all fields."

    return render_template("auth.html", title="Sign In / Sign Up", message=message)


if __name__ == "__main__":
    app.run(debug=True)
