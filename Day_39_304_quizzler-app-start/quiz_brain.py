import html


class QuizBrain:

    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list
        self.current_question = None

    def still_has_questions(self):
        """남은 질문이 있는지 확인합니다."""
        return self.question_number < len(self.question_list)

    def next_question(self):
        """다음 질문을 가져와 형식을 맞춰 반환합니다."""
        if self.still_has_questions():
            self.current_question = self.question_list[self.question_number]
            self.question_number += 1
            # HTML 엔티티를 unescape하여 깨끗한 텍스트로 변환합니다.
            q_text = html.unescape(self.current_question.text)
            return f"Q.{self.question_number}: {q_text}"
        else:
            return "퀴즈가 끝났습니다!"

    def check_answer(self, user_answer: str) -> bool:
        """사용자의 답변을 확인하고 점수를 업데이트한 뒤, 정답 여부를 반환합니다."""
        correct_answer = self.current_question.answer
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        else:
            return False
