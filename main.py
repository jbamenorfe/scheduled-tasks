""" This program sends a birthday email to the user's family members and friends
Author:     Joshua Bright Amenorfe
Date:       17/03/2026"""

import pandas as pd
import datetime as dt
import smtplib, ssl
from email.message import EmailMessage
import random
import os

#   Create a datetime object called now
now = dt.datetime.now()
today_month = now.month
today_day = now.day
today = (today_month, today_day)        # Create a tuple of month and day

#   Use pandas to read the birthdays.csv
birthdays = pd.read_csv('birthdays.csv')

#   Convert the read .csv file to a dictionary
birthdays_dict = { (row.month, row.day): row for (index, row) in birthdays.iterrows()}

if (today_month, today_day) in birthdays_dict:      #   Check to see if the month and day are in dictionary
    celebrant_name = birthdays_dict[(today_month, today_day)]["name"]       # Celebrant name is name of person whose
    # birthday and birthmonth are found in the dictionary
    celebrant_email = birthdays_dict[(today_month, today_day)]["email"]     # Celebrant's emial is the email of the
    # person whose birthmonth and birthday are found in the dictionary
    letter_num = random.randint(1,3)        # Generate a random integer

    with open(f"letter_templates/letter_{letter_num}.txt", "r") as file:    # Use the random integer to select a letter
        letter = file.read()        # Read the letter
        letter_to_send = letter.replace("[NAME]", celebrant_name)   # Replace the salutation on the chosen template

        sender_email = "pymailcoder@gmail.com"
        receiver_email = celebrant_email
        app_password = "ioojlqwzptpzhubg"

        msg = EmailMessage()
        msg.set_content(letter_to_send)

        msg['Subject'] = f"Happy Birthday! {celebrant_name}!"
        msg['From'] = sender_email
        msg['To'] = receiver_email
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, app_password)
                server.send_message(msg)
                print("Email sent successfully")

        except Exception as e:
            print(f"An error occurred: {e}")
