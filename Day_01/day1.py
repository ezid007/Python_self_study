import random

scissors = '''
     _______
----'   ____)____
          ______)
       __________)
      (____)
----.___

'''

rock = '''
     _______
----'   ____)
      (_____)
      (_____)
      (____)
----.___

'''

paper = '''
     _______
----'   ____)____
          ______)
          _______)
         _______)
----.__________)

'''

all_list = [scissors,rock,paper]

all_list[random.randint(0,2)]

print(all_list[1])


