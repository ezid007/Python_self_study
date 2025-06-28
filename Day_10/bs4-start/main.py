from bs4 import BeautifulSoup


with open("Self_study\\Day_10\\bs4-start\\website.html", encoding="utf-8") as file:
    contents = file.read()
    
soup = BeautifulSoup(contents, "html.parser")

all_anchor_tags = soup.find_all("a")

h3_heading = soup.find(name="h3", class_="heading")
print(h3_heading)

company_url = soup.select_one("#name")
# print(company_url)

heading = soup.select(".heading")
# print(heading)

# for h in soup.select(".heading"):
    # print(h.text)