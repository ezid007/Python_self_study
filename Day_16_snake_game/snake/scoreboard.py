import json
from turtle import Turtle

LEADERBOARD_FILE = "self_study\\Day_16\\snake\\scores.json"
LEADERBOARD_FONT = ("Courier", 16, "normal")
ALIGNMENT = "center"
FONT = ("Courier", 24, "normal")

class Scoreboard(Turtle):
    
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("white")
        self.penup()
        self.goto(0, 260)
        self.hideturtle()
        self.update_scoreboard()
        
    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)
        
    def increase_score(self):
        self.score += 1
        self.update_scoreboard()
    
    def load_scores(self):
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_score(self, name):
        scores = self.load_scores()
        scores.append({"name":name, "score":self.score})
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
            json.dump(scores, file, indent=4)

    def display_leaderboard(self):
        self.clear()
        self.goto(0, 260)
        self.write("Leaderboard", align=ALIGNMENT, font=FONT)
        
        scores = self.load_scores()
        scores.sort(key=lambda item: item['score'], reverse=True)
        
        y_position = 220
        
        for i, record in enumerate(scores[:10]):
            self.goto(0, y_position)
            rank_text = f"{i+1}. {record['name']}: {record['score']}"
            self.write(rank_text, align=ALIGNMENT, font=LEADERBOARD_FONT)
            y_position -= 30

