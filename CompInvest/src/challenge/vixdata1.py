#!/usr/bin/env python
import sys
import datetime
import smtplib
import ystockquote
import time
from email.mime.text import MIMEText
t0 = time.time()
# ticker to look up
ticker1 = '^VIX'
ticker2 = '^VXV'
ticker3 = 'ZIV'
# number of days of historical data to fetch (not counting today)
days_back = 30
email_from = 'XXXX@gmail.com'
email_to = 'YYYY@gmail.com'
#today's date
end = datetime.date.today()
#30 days ago from today - need more days to account for weekends, market close days
start = datetime.date.today() + datetime.timedelta(days = -days_back)
# fetch the historical data from yahoo
vixdata = ystockquote.get_historical_prices(ticker1, start.strftime("%Y%m%d"), end.strftime("%Y%m%d"))
vxvdata = ystockquote.get_historical_prices(ticker2, start.strftime("%Y%m%d"), end.strftime("%Y%m%d"))
zivdata = ystockquote.get_historical_prices(ticker3, start.strftime("%Y%m%d"), end.strftime("%Y%m%d"))
msgtext = "Market close data from Yahoo Finance"
# print 14 days of data to email message
for i in range(1, 16):
    msgline =  str(vixdata[i][0]) + "  VIX: " + str(vixdata[i][4]) + "  VXV: "+ str(vxvdata[i][4]) + "  Ratio: %.2f" % (float(vixdata[i][4])/float(vxvdata[i][4])) + "  ZIV: " + str(zivdata[i][4])
    msgtext = msgtext + "\n" + msgline
#
print msgtext
#send email message
gmail_user = email_from
gmail_pwd = "XXXX"
FROM = gmail_user
TO = [email_to] #must be a list
SUBJECT = "VIXDATA Update"
TEXT = msgtext
# Prepare actual message
message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
          """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
try:
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
    server.quit()
    print 'successfully sent the mail'
except:
    print "failed to send mail"
print str(round(time.time() - t0 , 2)) + ' seconds to process'
