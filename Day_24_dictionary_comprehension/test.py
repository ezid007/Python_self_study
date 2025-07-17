import pandas as pd

student_dict = {
    "student": ["Angela", "James", "Lily"],
    "score": [56, 76, 98]
}
student_df = pd.DataFrame(student_dict).set_index("student")

"""
.iterrows()를 사용하여 각 학생(인덱스)과 점수(행 데이터)를 출력합니다.
"""
for student_name, row_data in student_df.iterrows():
    print(f"--- {student_name} 학생의 정보 ---")
    print("전체 행 데이터 (시리즈 객체):")
    print(row_data)
    print(f"점수만 따로 확인: {row_data['score']}")
    print("\n")