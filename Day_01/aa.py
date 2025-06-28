student_heights = ['151', '145', '179']
# student_heights = input().split() 인풋을 받아서 공백을 기준으로 나눌 때 사용. split('.') 나눌 기준은 다른 것으로 바꾸는게 가능하다.

# for n in range(0, len(student_heights)):
#     student_heights[n] = int(student_heights[n])
total = 0
my_ever = 0

for i, height in enumerate(student_heights):
    student_heights[i] = int(height)
    total += height
 
 
my_ever = total / len(student_heights) *100


    
my_ever