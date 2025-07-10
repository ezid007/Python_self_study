from rich import print
import requests
import os

os.system("cls")

# if response.status_code == 404:
#     raise Exception("That resource does not exist.")
# elif response.status_code == 401:
#     raise Exception("You are not authorised to access this data.")

try:
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

except requests.exceptions.HTTPError as err:
    print(f"HTTP 에러가 발생했습니다: {err}")

except requests.exceptions.RequestException as err:
    print(f"요청 중 에러가 발생했습니다: {err}")

else:
    longitude = response.json()["iss_position"]["longitude"]
    latitude = response.json()["iss_position"]["latitude"]
    iss_locate = (latitude, longitude)
    print(iss_locate)
