# from data import question_data
from question_model import Question
from quiz_brain import QuizBrain
import requests

API_URL = "https://opentdb.com/api.php?amount=10&type=boolean"

response = requests.get(API_URL)
response.raise_for_status()
data = response.json()

question_data = [
    {"text": question["question"],
     "answer": question["correct_answer"]}
    for question in data["results"]
]


question_bank = []

for question in question_data:
    question_text = question["text"]
    question_answer = question["answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)

quiz = QuizBrain(question_bank)

while quiz.still_has_questions():
    quiz.next_question()

print("You've completed the quiz")
print(f"Your final score was: {quiz.score}/{quiz.question_number}")