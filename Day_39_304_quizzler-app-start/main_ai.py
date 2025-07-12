# 필요한 클래스와 라이브러리를 가져옵니다.
# Question: 질문 텍스트와 답변을 저장하는 클래스
# QuizBrain: 퀴즈 진행 로직을 담당하는 클래스
# requests: API에 HTTP 요청을 보내기 위한 라이브러리
# html: HTML 특수 문자를 일반 문자로 변환하기 위한 라이브러리
from question_model import Question
from quiz_brain import QuizBrain
import requests
import html

""" --- 1. 퀴즈 준비 --- """
# QuizBrain 객체를 생성합니다.
# 처음에는 질문 목록이 비어있으므로 빈 리스트 '[]'를 전달합니다.
# 질문은 퀴즈를 진행하면서 실시간으로 하나씩 추가될 것입니다.
quiz = QuizBrain([])

""" --- 2. 퀴즈 루프 시작 --- """
# 10개의 질문을 풀기 위해 for 반복문을 10번 실행합니다.
# 'range(10)'의 숫자를 바꾸면 전체 퀴즈의 길이를 조절할 수 있습니다.
for question_index in range(10):

    """--- 3. 실시간으로 질문 1개 가져오기 ---"""
    # OpenTDB API에 요청을 보내 '참/거짓' 유형의 질문 1개를 받아옵니다.
    response = requests.get("https://opentdb.com/api.php?amount=1&type=boolean")

    # 만약 API 요청에 문제가 생기면 (예: 인터넷 연결 오류) 프로그램을 중단시킵니다.
    response.raise_for_status()

    # 받아온 데이터(JSON 형식)에서 실제 질문 정보가 담긴 부분을 추출합니다.
    data = response.json()["results"][0]

    """ --- 4. 질문 데이터 처리 및 객체 생성 --- """
    # 질문 텍스트에 포함된 특수 HTML 문자(예: &quot;)를 일반 문자(예: ")로 변환합니다.
    question_text = html.unescape(data["question"])
    # 정답 텍스트를 가져옵니다.
    question_answer = data["correct_answer"]

    # 처리된 질문 텍스트와 정답으로 새로운 Question 객체를 만듭니다.
    new_question = Question(question_text, question_answer)

    """ --- 5. 질문 목록에 새 질문 추가 및 문제 출제 --- """
    # 방금 만든 새로운 질문 객체를 QuizBrain의 질문 목록에 추가합니다.
    quiz.question_list.append(new_question)

    # QuizBrain의 next_question 메서드를 호출하여 사용자에게 문제를 냅니다.
    # 이 메서드는 현재 문제 번호에 해당하는 질문을 목록에서 찾아 출력합니다.
    quiz.next_question()


""" --- 6. 퀴즈 종료 및 결과 발표 --- """
# for 반복문이 모두 끝나면, 퀴즈가 완료되었음을 알립니다.
print("\nYou've completed the quiz")
# 최종 점수를 '맞힌 개수 / 전체 문제 수' 형식으로 출력합니다.
print(f"Your final score was: {quiz.score}/{quiz.question_number}")
