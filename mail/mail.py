# import sys
# sys.path.append("..")
import yagmail
from error import ErrorModal
from CONSTANT.index import *
class DigixMail():
    def __init__(self, reciever_email, subject, message, attachments=[]):
        self.sender_mail = APP_SMTP_MAIL_SENDER_MAIL_ID  
        self.mail_password = APP_SMTP_MAIL_PASSWORD
        self.reciever_mail = reciever_email
        self.message = message
        self.message_subject = subject
        self.attachments = attachments
        self.execute_mail()
        
    def execute_mail(self):
        try:
            # initiating connection with SMTP server
            yagmail.register(self.sender_mail, self.mail_password)
            yagmail_instance = yagmail.SMTP(self.sender_mail)
            
            # Adding Content and sending it
            yagmail_instance.send(
                to=self.reciever_mail,
                subject=self.message_subject,
                contents=self.message, 
                attachments=self.attachments,
            )

        except Exception as error:
            print(f"Development Error (While Sending Mail) = {error}")
            ErrorModal("Something went wrong, please try again.")
                    
