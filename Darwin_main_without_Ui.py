import tkinter
import sys
import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button
import threading
import queue

import colorama
from colorama import Fore, Back, Style

# Initialize colorama to work with ANSI escape codes
colorama.init()




# Path: Darwin\Alan\Alan_main.py



#!Importing all files manually because of the way the program is structured
import sys
sys.path.append("D:\\Daniyals Stuffs\\A.I learning\Darwin\\Functionalities\\Document_Process.py")
sys.path.append("D:\\Daniyals Stuffs\\A.I learning\\Darwin")

#sys.path.append("F:\\A.I learning\\Alan")
sys.path.append("D:\\Daniyals Stuffs\\A.I learning\\Darwin\\Basic_nlp_functions.py")
sys.path.append("D:\\Daniyals Stuffs\\A.I learning\\Darwin\\Functionalities\\Gmail.py")
sys.path.append("D:\\Daniyals Stuffs\\A.I learning\\Alan\\Alan_main.py")



#!Importing necessary files
from Intent_recog import *
from Alan_.Alan_main import *
from Basic_nlp_functions import *
from Functionalities.Gmail import *
from Functionalities.Notion import *




#!The Darwin_bot, the first pipeline through which the user input is fed
class Darwin_bot:
 

    
    def __init__(self):
        #!Initializing the Alan bot
        self.alan_bot = Alan()

        #!JUST FOR EMAILS

        
        #!Consider past response is a boolean that tells the bot if it should consider the past response, this helps it have some sort of short term memory
        #!Further more if the bot needs a true or false response it knows how to bounce back the the function after returing the response
        self.consider_past_response = 1
        #!conservation is appended to let the bot know if it should consider the past responses, and have some sort of short term memory

        self.conversation = []  
        self.past_classifications = []    


    #!The main function that processes the user input
    def Darwin_Process(self,user_input):
        response = ""

        #!First it checks if it should consider past ressponses, this usually happens when the bot needs some more of response when it asked a 
        #!question
        if(self.consider_past_response >1):
                if(self.past_classifications[-1]=="email_requests"):
                    response= self.email_requests(user_input,self.conversation[-1])


        else:
            #!Other wise it should use the distill_bert model to identify the intent
            result=identify_intent(user_input)



        #!If the score is greater than .7 then it should consider the response as a true response and not feed it to Alan
        #! The point of this is to give control to some aspects that alan is not capable of doing
            if(result[0]['score']>.9):
                 self.past_classifications.append(result[0]['label'])
                 print("functions will go here")
                 if(result[0]['label']=="Turn_on_internet"):
                    response=  self.alan_bot.Switch_internet()
                 elif(result[0]['label']=="Turn_off_internet"):
                    response=  self.alan_bot.Switch_internet()
                 elif(result[0]['label']=="email_requests"):
                     response= self.email_requests(user_input)
                 elif(result[0]['label']=="Save_Response"):
                    response= self.save_response(user_input)

                 elif(result[0]['label']=="Notion_edit"):
                    response= self.notion_edit(user_input)
                    print("Function goes here")




            else:
                 self.past_classifications.append("Alan")
                 print("Feeding to Alan")
                 self.consider_past_response= 1
                 response = self.alan_bot.ProcessResponse(user_input)
                 #response = "Alan is not responding right now"
          
                #!if the response meets the geared_responses requirements then it should be fed to the geared_responses model



        self. conversation.append(response)
        print(response)


    def notion_edit(self,user_input):
        Date = fetch_labels(user_input, "DATE", undefined="UNKNOWN")
        Keywords = Basic_Keyword_Extractor(user_input)
        if(Date == "UNKNOWN"):
            add_event(Keywords)

        else:
            add_event(Keywords,Date)


        return "Okay I added that to your calender"

        



    


    def save_response(self,user_input):
        file_types = ["pdf","docx","txt"]


        if(self.consider_past_response== False and user_input.lower() not in file_types):
            self.consider_past_response = True
            return "What would you like to save this as"
        
        else:
            self.consider_past_response= False
            return "Feature not implemented yet"
        
    def email_requests(self,user_input):

        sender = "Daniyal Ahmed"
        

        body = self.alan_bot.ProcessResponse(user_input +"Make sure to start your email with \'Dear Sir/Madam\'")
        

        email = Gmail(user_input, body)


       
        user_input2= input("Would you like to send this email ")

        if(Affirm_or_deny(user_input2)=="yes"):
    
                if(email.reciever_email=="UNKNOWN" or email.reciever_name=="Name"):
                    while True:
                        print("stuck here 2nd loop")
                        if(str(email.reciever_email)=="UNKNOWN" and str(email.reciever_name)!="Name"):
                            user_input= input("What is the email?\n")
                            email.reciever_email = str(fetch_labels(user_input, "EMAIL", undefined="UNKNOWN"))
                        elif(str(email.reciever_email)!="UNKNOWN" and str(email.reciever_name)=="Name"):
                            user_input= input("Who is the Email For\n")
                            email.reciever_name = fetch_labels(user_input, "PERSON", undefined="Name")
                        elif(str(email.reciever_email)=="UNKNOWN" and str(email.reciever_name)=="Name"):
                            user_input= input("Who is the Email For, Please write the email as well\n")
                            receiver_email = fetch_labels(user_input, "PERSON", undefined="Name")
                            email.reciever_name = fetch_labels(user_input, "PERSON", undefined="Name")
                            email.reciever_email = fetch_labels(user_input, "EMAIL", undefined="UNKNOWN")
                     
                        elif(str(email.reciever_email)!="UNKNOWN" and str(email.reciever_name)!="Name"):
                             print("Hit last elif")
                             break
                        
            




                email.body = "Dear "+ str(email.reciever_name) + ",\n\n" + email.body+"\nRegards,\n"+sender
                print( email.send_email("No-Subject", email.body, str(email.reciever_email)))


               








Darwin = Darwin_bot()



while True:
    input1 = input("What would you like to do\n")
    
    Darwin.Darwin_Process(input1)





def print_color(text, fore_color=Fore.WHITE, back_color=Back.BLACK, style=Style.NORMAL):
    formatted_text = f"{style}{fore_color}{back_color}{text}{Style.RESET_ALL}"
    print(formatted_text)

# Example usage:
