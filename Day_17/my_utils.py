# my_utils.py

import builtins # 파이썬의 원래 내장 함수들에 접근하기 위함

def print(text, style="normal"):
    """
    이모지를 붙여주는 나만의 특별한 print 함수
    """
    prefix = "✨ " # 기본 접두사

    if style == "warning":
        prefix = "⚠️ "
    elif style == "error":
        prefix = "🔥 "
    
    # 원래의 print 함수를 호출해서 최종적으로 출력
    builtins.print(prefix + str(text))