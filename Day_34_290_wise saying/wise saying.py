import smtplib
import datetime
import random

MY_EMAIL = "appbreweryinfo@gmail.com"
MY_PASSWORD = "abcd1234()"

new = datetime.datetime.now()
weekday = new.weekday()

if weekday == 1:
    with open("self_study/Day_34_290_wise saying/quotes.txt") as quote_file:
        all_quotes = quote_file.readline()
        quote = random.choice(all_quotes)
    print(quote)

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:Monday Motivation\n\n{quote}",
        )

