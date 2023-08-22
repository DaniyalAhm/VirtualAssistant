import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import sys

sys.path.append("C:\\Users\\eggsc\\Documents\\A.I learning\\U.i\\Ui v.1.py")
sys.path.append("C:\\Users\\eggsc\\Documents\\A.I learning\\Alan")
sys.path.append("C:\\Users\\eggsc\\Documents\\A.I learning\\Darwin\\Basic_nlp_functions.py")
sys.path.append("C:\\Users\\eggsc\\Documents\\A.I learning\\U.i")



from Basic_nlp_functions import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Gmail:



    def __init__(self,user_input,email):
        self.body, self.reciever_email, self.reciever_name = self.Analyze_Email(user_input, email, "all")




    def send_email(self,subject, email_body, recipient_email):
        sender_email = 'ahmeddaniyal265@gmail.com'
        sender_password = 'xlxhcdunzytitufr'
    
        # Create a MIMEText object to represent the email
        email_subject = generate_title(email_body,20)
        email_body = email_body
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = email_subject
        msg.attach(MIMEText(email_body, 'plain'))

        # Send the email using Gmail's SMTP server
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  # Encrypt the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()
            return "Email sent successfully!"
        except Exception as e:
            return "Email not sent", e

    def Analyze_Email(self, user_input, email, lookfor='all'):
     
        #Body = Body[1]

        if(lookfor == "all"):
            Body = self.get_body(email)
            print(Body)

            receiver_email = fetch_labels(user_input, "EMAIL", undefined="UNKNOWN")
            print(receiver_email)
            self.reciever_name = fetch_labels(user_input, "PERSON", undefined="Name")
            print(self.reciever_name)
            return [Body, receiver_email, self.reciever_name]

        elif(lookfor.lower() == "email"):
            return  fetch_labels(user_input, "EMAIL", undefined="UNKNOWN")

        elif(lookfor.lower() == "name"):
            return fetch_labels(user_input, "PERSON", undefined="Name")
        


    def get_body(self, email):
        Body = email.split("\n\n")
        Bodystr = ""
        for x in Body: 
                if x[-1]=="." or x[-1]=="!" or x[-1]=="?":
                    Bodystr= Bodystr + x


        return Bodystr
            



    '''
    def email_requests(self, user_input):
        sender = "Daniyal"
        print(self.reciever_name)

        if self.reciever_email == "UNKNOWN" or self.reciever_name == "Name":
            if self.reciever_email == "UNKNOWN" and self.reciever_name != "Name":
                self.reciever_name_=self.Analyze_Email(user_input,  self.body, lookfor='name')
            elif self.reciever_email != "UNKNOWN" and self.reciever_name == "Name":
                self.reciever_email_=self.Analyze_Email(user_input,  self.body, lookfor='email')

            elif self.reciever_email == "UNKNOWN" and self.reciever_name == "Name":
                self.reciever_email_=self.Analyze_Email(user_input,  self.body, lookfor='email')
                self.reciever_name_=self.Analyze_Email(user_input,  self.body, lookfor='name')

        if self.reciever_email == "UNKNOWN" or self.reciever_name == "Name":
            if self.reciever_email == "UNKNOWN" and self.reciever_name != "Name":
                return ("What is the email?")
            elif self.reciever_email != "UNKNOWN" and self.reciever_name == "Name":
                return ("Who is the Email For")
            elif self.reciever_email == "UNKNOWN" and self.reciever_name == "Name":
               return ("Who is the Email For, Please write the email as well")
           



        if "[Name]" in email:
            email = email.replace("Dear [Name]", self.reciever_name)


        return  self.send_email("No-Subject", email, self.reciever_email)
    '''
            
