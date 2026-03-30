import smtplib

server = smtplib.SMTP("mail.privateemail.com", 587)
server.starttls()
server.login("info@varyon-hrmis.com", "Dev.25-erphrims")

r = server.sendmail(
    "info@varyon-hrmis.com",
    "eczbright@gmail.com",
    "Subject: Test\n\nHello from Python"
)

print (r)

server.quit()