# converter.py
import base64

# 변환할 아이콘 파일 경로
ICON_FILE_PATH = (
    "self_study\\Day_27_257_the_pomodoro_technique\\data_base64\\tomato.ico"
)
# 결과를 저장할 텍스트 파일 이름
OUTPUT_TXT_FILE = "icon_data.txt"

try:
    # 1. 아이콘 파일을 바이너리 읽기 모드('rb')로 엽니다.
    with open(ICON_FILE_PATH, "rb") as icon_file:
        binary_data = icon_file.read()
        base64_data = base64.b64encode(binary_data).decode("utf-8")

    # 2. 저장할 전체 내용을 f-string으로 만듭니다.
    content_to_save = f'ICON_DATA = """{base64_data}"""'

    # 3. 새로운 .txt 파일을 쓰기 모드('w')로 열고 내용을 저장합니다.
    with open(OUTPUT_TXT_FILE, "w") as txt_file:
        txt_file.write(content_to_save)

    print(f"✅ 성공! '{OUTPUT_TXT_FILE}' 파일에 Base64 데이터가 저장되었습니다.")
    print("이 파일의 내용을 복사하여 'code_data.py'에 붙여넣으세요.")

except FileNotFoundError:
    print(
        f"❌ 오류: '{ICON_FILE_PATH}' 파일을 찾을 수 없습니다. 파일 이름과 경로를 확인하세요."
    )
