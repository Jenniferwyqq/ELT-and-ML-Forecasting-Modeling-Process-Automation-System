import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_email():
    try:
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        message = "<html><head></head><body><p>Hi Jennifer,</p><p>Belows are the prediction result for top 25 products in the week of 2020/10/12.</p><table border=\"1\"><tr><th>Category</th><th>Color</th><th>Material</th><th>quantity</th></tr>";
        with open('Results.csv', 'r') as c:
            reader = csv.reader(c)
            for row in reader:
                quantity = row[0]
                category = row[2]
                color = row[3]
                material = row[4]
                cur = "<tr><td>" + category + "</td><td>" + color + "</td><td>" + material + "</td><td>" + quantity + "</td></tr>";
                message += cur 
        message += "</table><p>Sincerely,</p><p>Jenni</p></body></html>"
        me = "chihyi1126@gmail.com"
        you = "chihyi1126@gmail.com"
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "ML forecasting for the sales of 25 top products next week"
        msg['From'] = me
        msg['To'] = you
        html_message = MIMEText(message, 'html')
        msg.attach(html_message)

        x=smtplib.SMTP('smtp.gmail.com', 587)
        x.starttls()
        x.login("chihyi1126@gmail.com", "dbxiksppknxkkqdh")
        x.sendmail(me, you, msg.as_string())
        x.quit()
        print("Success")
    except Exception as exception:
        print(exception)
        print("Failure")