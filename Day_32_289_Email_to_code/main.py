import smtplib
from email.message import EmailMessage

# --- 1. 기본 정보 설정 ---
# 보내는 사람 이메일
MY_EMAIL = "나의 네이버 이메일"
# 1단계에서 발급받은 16자리 앱 비밀번호를 여기에 입력하세요.
# 보안을 위해 input() 보다는 직접 코드에 넣거나 환경 변수를 사용하는 것이 더 일반적입니다.
APP_PASSWORD = "DZXCEBHBYD2K"
# 받는 사람 이메일
RECIPIENT_EMAIL = "받을 사람 이메일"

# --- 2. 이메일 메시지 생성 ---
# EmailMessage 객체를 사용하면 제목, 본문, 인코딩 등을 쉽게 관리할 수 있습니다.
msg = EmailMessage()
msg["Subject"] = "파이썬으로 보내는 자동 메일 테스트"  # 메일 제목
msg["From"] = MY_EMAIL  # 보내는 사람
msg["To"] = RECIPIENT_EMAIL  # 받는 사람
msg.set_content("이 메일은 파이썬 코드를 통해 자동으로 발송되었습니다.")  # 메일 본문

# --- 3. 네이버 SMTP 서버에 연결하고 메일 발송 ---
try:
    # 네이버 SMTP 서버 주소와 포트 번호입니다.
    # smtplib.SMTP(서버주소, 포트)
    with smtplib.SMTP("smtp.naver.com", 587) as smtp:
        # SMTP 연결을 암호화된 통신으로 전환합니다. (필수)
        smtp.starttls()
        # 발급받은 앱 비밀번호로 로그인합니다.
        smtp.login(MY_EMAIL, APP_PASSWORD)
        # 생성한 메시지 객체를 사용해 메일을 발송합니다.
        smtp.send_message(msg)
        print("메일 발송에 성공했습니다!")

except Exception as e:
    print(f"메일 발송에 실패했습니다: {e}")
