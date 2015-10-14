'''
Created on Nov 3, 2014

@author: adrian
'''
import sys
import smtplib
from email.mime.text import MIMEText
#
def sendGmail(email_from, email_to, subjectText, messageText):
    gmail_user = email_from
    gmail_pwd = "Rea1Estate" #(could be stored separately if security is an issue)
    FROM = gmail_user
    TO = [email_to] #must be a list
    SUBJECT = subjectText
    TEXT = messageText
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
        print "Error: %s" % sys.exc_info()[0]        
        print "Error: %s" % sys.exc_info()[1]        
        print "Error: %s" % sys.exc_info()[2]        
      
        print "failed to send mail, try this https://support.google.com/accounts/answer/6010255"
# end Def sendGmail

 
if __name__ == '__main__':
    #
    # Test program
    email_from = 'mr.sarno2@gmail.com'
    email_to = 'adriansarno@hotmail.com'
    subjectText = 'Test Gmail Message'
    messageText = 'Please look at XXX for recent event trigger'
    #
    sendGmail(email_from,email_to,subjectText,messageText)