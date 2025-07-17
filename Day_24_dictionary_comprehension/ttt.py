import pandas as pd

student_dict = {
    "student": ["Angela", "James", "Lily"],
    "score": [56, 76, 98]
}
student_df2 = pd.DataFrame(student_dict)

student_df2.iloc[2,0] = 80

for index, row in  student_df2.iterrows():
    if row.student == "Angela":
        print(row.score)
        