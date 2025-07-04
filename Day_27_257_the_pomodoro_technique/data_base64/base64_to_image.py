import base64

# 변환하고 싶은 이미지 파일 경로
image_path = 'self_study/Day_27_257_the_pomodoro_technique/tomato.png'
output_txt_name = "self_study/Day_27_257_the_pomodoro_technique/tomato.txt"

# 이미지 파일을 바이너리 읽기 모드('rb')로 열어서 Base64로 인코딩합니다.
with open(image_path, 'rb') as image_file:
    # base64.b64encode() 함수로 인코딩하고,
    # .decode('utf-8')을 통해 우리가 사용할 수 있는 utf-8 문자열로 변환합니다.
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

with open(output_txt_name, "w") as txt_file:
    txt_file.write(encoded_string)

print(f"'{image_path}' 파일을 인코딩하여 '{output_txt_name}' 파일에 저장했습니다!")