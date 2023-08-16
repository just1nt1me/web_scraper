import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email_config import pswd, users
from datetime import datetime
from oakhouse import Oakhouse
import os
import sys

# Setup port number and server name

smtp_port = 587                 # Standard secure SMTP port
smtp_server = "smtp.gmail.com"  # Google SMTP Server

# Set up the email lists
email_from = "jccarville@gmail.com"
email_list = users

# name the email subject
now = datetime.now()
subject = f"{now} Oakhouse Vacancies"

# Define the email function (dont call it email!)
def send_emails(email_list):

    # Connect with the server
    print("Connecting to server...")
    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
    TIE_server.starttls()
    TIE_server.login(email_from, pswd)
    print("Succesfully connected to server")
    print()

    for person in email_list:

        # Make the body of the email
        body = f"Today's Oakhouse Vacancies"

        # make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = person
        msg['Subject'] = subject

        # Attach the body of the message
        msg.attach(MIMEText(body, 'plain'))

        # Define the file to attach
        path = os.getcwd()
        filename = os.path.join(path, 'oakhouse_vacancies.txt')

        # Open the file in python as a binary
        with open(filename, 'rb') as attachment:
        # attachment= open(filename, 'rb')  # r for read and b for binary

            # Encode as base 64
            attachment_package = MIMEBase('application', 'octet-stream')
            attachment_package.set_payload((attachment).read())
            encoders.encode_base64(attachment_package)
            attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
            msg.attach(attachment_package)

            # Cast as string
            text = msg.as_string()


        # Send emails to "person" as list is iterated
        print(f"Sending email to: {person}...")
        TIE_server.sendmail(email_from, person, text)
        print(f"Email sent to: {person}")
        print()

        # Close the port
        TIE_server.quit()


if __name__ == '__main__':
    Oakhouse().get_output()
    # Redirect the standard output back to the console
    sys.stdout = sys.__stdout__
    send_emails(email_list)
