#! /usr/bin/python3

import csv
import json
import smtplib
import ssl
import time
import schedule
import getpass
import covid19_data

data = covid19_data.dataByName("Malaysia")



message = """Subject: COVID-19 Daily Statistics

Hi {name}, Here are the COVID-19 statistics in Malaysia for today:

Total: {total}
Recovered: {recovered}
Deaths: {deaths}

Stay safe, always wear a mask!
Thank you!

"""

from_address = "<Enter email address>"
password = getpass.getpass(prompt='Password: ', stream=None)


def send_email():
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(from_address, password)
                with open("list.csv") as file:
                        reader = csv.reader(file)
                        next(reader)  # Skip header row
                        for name, email in reader:
                                server.sendmail(
                                        from_address,
                                        email,
                                        message.format(name=name, total=data.cases, recovered=data.recovered, deaths=data.deaths)
                                )

#run once                       
send_email()                                
print("Email sent")

schedule.every().day.at("19:00").do(send_email)
print("Schedule set for every day at 1900 to send email")

