from rich import print
import traceback


def function_a():
    print("function_a가 function_b를 호출합니다.")
    function_b()
    print("function_a가 종료됩니다.")


def function_b():
    print("function_b가 function_c를 호출합니다.")
    function_c()
    print("function_b가 종료됩니다.")


def function_c():
    print("function_c에서 오류를 발생시킵니다.")
    # 여기서 ZeroDivisionError 발생!
    result = 10 / 0
    return result


# 메인 코드
try:
    function_a()

except Exception:
    # 에러가 발생하면 상세 내용을 문자열로 가져와 출력
    error_details = traceback.format_exc()
    print("\n--- 에러 발생! 상세 정보 ---")
    print(error_details)
    print("--------------------------")
    # 이 정보를 파일에 기록하여 에러 로그를 만들 수 있습니다.
    # with open("error_log.txt", "a") as f:
    #     f.write(error_details + "\n")

print("프로그램이 정상적으로 종료되었습니다.")
