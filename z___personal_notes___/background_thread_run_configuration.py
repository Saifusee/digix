# from mail.mail import DigixMail
# import threading

# # Check each second if thread active or not  
# def schedule_check(self, t_hread):
#     self.after(1000, self.is_thread_complete, t_hread)
    
# # When Thread Complete 
# def is_thread_complete(self, t_hread):
#     if not t_hread.is_alive():
#         self.email_otp_button.configure(text="Submit E-Mail for OTP", state="normal")
#     else:
#         self.schedule_check(t_hread)

# reciver_email = "mohammadsaifulkhan9829@gmail.com"
# t_hread =threading.Thread(target=lambda: DigixMail(reciver_email, "Test Subject", "Hello Hello"), name="SendOTPMailThread")
# t_hread.start()
# schedule_check(t_hread)

    