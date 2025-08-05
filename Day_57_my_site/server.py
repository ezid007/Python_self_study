from flask import Flask, render_template
import random
import datetime
import requests

app = Flask(__name__)


@app.route("/")
def home():
    my_random = random.randint(1, 10)
    year = datetime.datetime.now().year
    return render_template("index.html", random_num=my_random, year=year)


@app.route("/guess/<name>")
def guess(name):
    gender_url = f"https://api.genderize.io?name={name}"
    gender_response = requests.get(gender_url)
    gender_data = gender_response.json()
    gender = gender_data["gender"]
    age_url = f"https://api.agify.io?name={name}"
    age_response = requests.get(age_url)
    age_data = age_response.json()
    age = age_data["age"]
    return render_template("guess.html", person_name=name, gender=gender, age=age)


@app.route("/blog")
def blog():
    blog_url = "https://api.npoint.io/047d9103b9753018c36b"
    response = requests.get(blog_url)
    all_posts = response.json()
    return render_template("blog.html", posts=all_posts)


if __name__ == "__main__":
    app.run(debug=True)
