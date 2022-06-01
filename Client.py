import requests

import smtplib

EMAIL_ADDRESS="draw.idf.io@gmail.com"
EMAIL_PASSWORD="a1234567!"

smtp=smtplib.SMTP('smtp.gmail.com',587)
smtp.ehlo()
smtp.starttls()
smtp.ehlo()
smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)

subject="Registered successfully to DRAWIO"
body="You have successfully logged in to DRAW.IO game, welcome!!"
msg=f'Subject: {subject}\n\n{body}'
response = requests.get("https://isitarealemail.com/api/email/validate",params = {'email': 'yoavkay@gmail.com'})
status = response.json()['status']
if status == "valid":
  print("email is valid")
else:
    print('fdffr')

#smtp.sendmail(EMAIL_ADDRESS,'yoavky@mai.com',msg)
