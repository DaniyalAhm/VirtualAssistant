import tkinter
import sys
import customtkinter as ct
import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button
import threading
import queue


# Path: Darwin\Alan\Alan_main.py



#!Importing all files manually because of the way the program is structured
import sys
'''
sys.path.append("C:\\Users\\eggsc\\Documents\\A.I learning\\U.i\\Ui V.2.py")
sys.path.append("C:\\Users\\eggsc\\Documents\\A.I learning\\Darwin\\Functionalities\\Document_Process.py")
sys.path.append("C:/Users/eggsc/Documents/A.I learning/Darwin/")
sys.path.append("C:/Users/eggsc/Documents/A.I learning/Alan/")
sys.path.append("C:/Users/eggsc/Documents/A.I learning/")
sys.path.append("C:\\Users\\eggsc\\Documents\\A.I learning\\Darwin\\Basic_nlp_functions.py")
sys.path.append("C:\\Users\eggsc\\Documents\\A.I learning\\Darwin\\Functionalities\\Gmail.py")
'''
#!Importing necessary files
from Intent_recog import *
from Alan_main import *
from Basic_nlp_functions import *
from Gmail import *

#!Global Variables
global Ignore_DarwinMain
Ignore_DarwinMain = False
global gblmessage
gblmessage = ""

 

def Ignore_DarwinMain_True():
    global Ignore_DarwinMain
    Ignore_DarwinMain = True
    print(f"Ignore_DarwinMain is {Ignore_DarwinMain}")


def Ignore_DarwinMain_False():
    global Ignore_DarwinMain
    Ignore_DarwinMain = False   
    print(f"Ignore_DarwinMain is now {Ignore_DarwinMain}")

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
            if(result[0]['score']>.7):
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
                    response= Notion_edit(user_input)




            else:
                 self.past_classifications.append("Alan")
                 print("Feeding to Alan")
                 self.consider_past_response= 1
          
                #!if the response meets the geared_responses requirements then it should be fed to the geared_responses model



        self. conversation.append(response)
        print_Darwin(response)



    def notion_edit(self,user_input):
        title = fetch_nouns(user_input)
        titlestr = ""
        for i in title:
            titlestr+=i+" "

        



    


    def save_response(self,user_input):
        file_types = ["pdf","docx","txt"]


        if(self.consider_past_response== False and user_input.lower() not in file_types):
            self.consider_past_response = True
            return "What would you like to save this as"
        
        else:
            self.consider_past_response= False
            return "Feature not implemented yet"
        
    def email_requests(self,user_input):
        sender = "Daniyal"
        reciever = "Name"
        receiver_email="UNKNOWN"


        email = self.alan_bot.ProcessResponse(user_input +"Make sure to start your email with \'Dear ["+reciever+"]\'")
        Ignore_DarwinMain_True()
        
        print_Darwin(email)

        email, receiver_email, reciever = Analyze_Email(user_input, email)

        print_Darwin("Would you like to send this email ")
        def email_thread(email,receiver_email,reciever):

            

                while True:        
                    print("stuck here 1st loop")
                    if(gblmessage!=""):
                        if(Affirm_or_deny(gblmessage)==True):
                             break
                        else:
                             return "Email not sent"
                
                if(receiver_email=="UNKNOWN" or reciever=="Name"):
                    while True:
                        print("stuck here 2nd loop")
                        if(receiver_email=="UNKNOWN" and reciever!="Name"):
                            user_input= input_darwin("What is the email?")
                            receiver = fetch_labels(user_input, "EMAIL", undefined="UNKNOWN")
                        elif(receiver_email!="UNKNOWN" and reciever=="Name"):
                            user_input= input_darwin("Who is the Email For")
                        elif(receiver_email=="UNKNOWN" and reciever=="Name"):
                            user_input= input_darwin("Who is the Email For, Please write the email as well")
                            receiver_email = fetch_labels(user_input, "PERSON", undefined="Name")
                            receiver_email = fetch_labels(user_input, "PERSON", undefined="Name")
                            receiver = fetch_labels(gblmessage, "EMAIL", undefined="UNKNOWN")
                     
                        elif(receiver_email!="UNKNOWN" and reciever!="Name"):
                             print("Hit  last elif")
                             break
                        
            

                if("[Name]" in email):
                    email = email.replace("Dear [Name]", reciever)


                    send_email("No-Subject", email, receiver_email)


                    return "Email Sent Successfully"
                else:
                    return "Email Not Sent"


        email_thread = threading.Thread(target=email_thread , args=(email, receiver_email, reciever))
    
        email_thread.start()









#!!! THE FUCKING Ui


Darwinbot = Darwin_bot()


ct.set_default_color_theme("green")
ct.set_appearance_mode("dark")

def send_message(event=None):
 
    message = entry.get()
    chat_area.configure(state=tk.NORMAL)
    chat_area.insert(tk.END, "You: " + message + "\n")
    chat_area.configure(state=tk.DISABLED)
    entry.delete(0, tk.END)

    receive_message(message= message)


    

def receive_message(message):
    global gblmessage
    global Ignore_DarwinMain

    if(Ignore_DarwinMain==True):

        message = "Ada:" + Darwinbot.Darwin_Process(message)
    chat_area.configure(state=tk.NORMAL)
    chat_area.insert(tk.END, message + "\n")
    chat_area.configure(state=tk.DISABLED)
    chat_area.place(x=40,y=10)
    gblmessage= message


def print_Darwin(message):
    print("Called print_Darwin")
    chat_area.configure(state=tk.NORMAL)
    chat_area.insert(tk.END, "Ada: " + message + "\n")
    chat_area.configure(state=tk.DISABLED)


def input_darwin(message):
    result_queue = queue.Queue()
    thread = threading.Thread(target=input_darwin_private , args=(message,))
    thread.start()  # Start the execution
    output = result_queue.get()
    return output
    
def input_darwin_private(str= ""):
    global gblmessage
    global Ignore_DarwinMain
    Ignore_DarwinMain = True
    if(str != ""):
        print_Darwin(str)

    while True:
        print("Waiting for input")
        while True:
            if(gblmessage!=""):
                return gblmessage 


def wait_for_input():
    message = entry.get()
    if message.strip():
        return (message)
    else:
        app.after(100, wait_for_input)  # Check for input again after 100 milliseconds






app = ct.CTk()
app.title("Ada A.I")
app.geometry("800x600")




chat_area = ct.CTkTextbox(app, height=500, width=700, wrap=tk.WORD, state=tk.DISABLED)
chat_area.pack(padx=10, pady=10, expand=True)
chat_area.place(x=40,y=10)


#chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

#scrollbar = Scrollbar(app, command=chat_area.yview)
#scrollbar.pack(padx=10, pady=10)

#scrollbar.grid(row=0, column=2, sticky="ns")
#chat_area["yscrollcommand"] = scrollbar.set

entry = ct.CTkEntry(app, width=600)
entry.pack(padx=5, pady=5,expand=True)
entry.place(x=40,y=520)
entry.place(x=40, y=520)
entry.bind("<Return>", send_message)  # Bind the <Return> event to send_message function.

#entry.grid(row=1, column=0, padx=10, pady=10)

send_button = ct.CTkButton(app, text="Send", width=80, command=send_message)
send_button.pack(padx=10, pady=10,expand=True)
send_button.place(x=660,y=520)



#send_button.grid(row=1, column=1, padx=0, pady=0)


app.mainloop()
