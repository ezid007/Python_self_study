from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("My_site.html")


if __name__ == "__main__":
    app.run(debug=True)
