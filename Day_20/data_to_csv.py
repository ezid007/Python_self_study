from rich import print
import pandas as pd
import os

os.system('cls')

WEATHER_DATA_CSV = 'self_study/Day_20/weather_data.csv'

weather_data = [
    ['day', 'temp', 'condition','냐하'],
    ['Monday', 12, 'Sunny','마마'],
    ['Tuesday', 14, 'Rain','마마'],
    ['Wednesday', 15, 'Rain','마마'],
    ['Thursday', 14, 'Cloudy','마마'],
    ['Friday', 21, 'Sunny','마마'],
    ['Saturday', 22, 'Sunny','마마'],
    ['Sunday', 24, 'Sunny','마마']
]

weather_data_pd = pd.DataFrame(weather_data[1:], columns=weather_data[0])

weather_data_pd.set_index('day', inplace=True)

weather_data_pd.to_csv(WEATHER_DATA_CSV, encoding='utf-8-sig')

PD_W_DATA = pd.read_csv(WEATHER_DATA_CSV)

temp_list = PD_W_DATA["temp"].to_list()

print(max(temp_list))
