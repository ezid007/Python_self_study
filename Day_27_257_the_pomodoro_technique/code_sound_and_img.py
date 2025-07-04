from code_data import sound_data, img_data
import base64
import simpleaudio as sa
import io


current_play_obj = None  # 현재 재생 중인 소리 객체를 저장할 변수


def play_sound_from_memory():
    global current_play_obj

    if current_play_obj and current_play_obj.is_playing():
        return

    try:
        decoded_audio_data = base64.b64decode(sound_data)
        wave_obj = sa.WaveObject.from_wave_file(io.BytesIO(decoded_audio_data))
        current_play_obj = wave_obj.play()

    except Exception as e:
        print(f"오류 방생:{e}")
        current_play_obj = None


def stop_sound():

    global current_play_obj

    if current_play_obj and current_play_obj.is_playing():
        current_play_obj.stop()


def img():
    return base64.b64decode(img_data)
