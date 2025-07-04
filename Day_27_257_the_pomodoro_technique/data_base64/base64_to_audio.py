# 1회용 코드: audio_to_txt.py
import base64

audio_file_name = "self_study/Day_27_257_the_pomodoro_technique/Work Music.wav"
output_txt_name = "self_study/Day_27_257_the_pomodoro_technique/alarm_sound.txt"

# 'rb'는 파일을 바이너리(binary) 읽기 모드로 연다는 뜻입니다.
with open(audio_file_name, "rb") as audio_file:
    # 오디오 파일을 읽어서 base64로 인코딩합니다.
    encoded_string = base64.b64encode(audio_file.read()).decode("utf-8")

# 'w'는 쓰기 모드로 파일을 연다는 뜻입니다.
# 인코딩된 텍스트를 txt 파일에 저장합니다.
with open(output_txt_name, "w") as txt_file:
    txt_file.write(encoded_string)

print(f"'{audio_file_name}' 파일을 인코딩하여 '{output_txt_name}' 파일에 저장했습니다!")
