from question_model import Question
from quiz_brain import QuizBrain
import requests

QUIZ_API = "http://opentdb.com/api.php?amount=1&type=boolean"

question_bank = []


def question():
    quiz_data = requests.get(QUIZ_API)
    question = quiz_data.json()["results"][0]
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)


quiz = QuizBrain(question_bank)

while quiz.still_has_questions():
    quiz.next_question()

print("You've completed the quiz")
print(f"Your final score was: {quiz.score}/{quiz.question_number}")

