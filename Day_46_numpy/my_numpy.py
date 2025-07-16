from rich import print
import numpy as np

py_list = [np.full(3, 8), np.array([33, -15, 26]), np.linspace(17, 26, 3)]

result_arr = []
for i in py_list:
    result_arr.append(np.mean(i))
    result_arr.append(np.std(i))
    result_arr.append(np.median(i))

print(result_arr)
