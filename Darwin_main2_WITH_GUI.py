import tkinter
import sys
import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button
import threading
import queue
import customtkinter as ct
import colorama
from colorama import Fore, Back, Style
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


#!Importing all files manually because of the way the program is structured EDIT had to revise the way the program was structured because of git difficulties
import sys
'''
sys.path.append("D:\\Daniyals Stuffs\\A.I learning\Darwin\\Functionalities\\Document_Process.py")
sys.path.append("D:\\Daniyals Stuffs\\A.I learning\\Darwin")

#sys.path.append("F:\\A.I learning\\Alan")
sys.path.append("D:\\Daniyals Stuffs\\A.I learning\\Darwin\\Basic_nlp_functions.py")
sys.path.append("D:\\Daniyals Stuffs\\A.I learning\\Darwin\\Functionalities\\Gmail.py")
sys.path.append("D:\\Daniyals Stuffs\\A.I learning\\Alan\\Alan_main.py")
'''


#!Importing necessary files
from Intent_recog import *
from Alan_main import *
from Basic_nlp_functions import *
from Gmail import *
from Notion import *
from ConversationDataStruct import *
from Question_Answering import *
from Document_Process import *











# Initialize colorama to work with ANSI escape codes
colorama.init()


message_queue = queue.Queue()
  # Start the execution




def print_color(text, fore_color=Fore.GREEN, back_color=Back.BLACK, style=Style.NORMAL):
    formatted_text = f"{style}{fore_color}{back_color}{text}{Style.RESET_ALL}"
    print(formatted_text)




def append_Darwin(text, conversation):
    chat_area.configure(state=tk.NORMAL)
    chat_area.insert(tk.END, "Darwin: " + str(text) + "\n")
    chat_area.configure(state=tk.DISABLED)
  







def send_message(event=None):
    global gblmessage
    message = entry.get()
    chat_area.configure(state=tk.NORMAL)
    chat_area.insert(tk.END, "You: " + message + "\n")
    chat_area.configure(state=tk.DISABLED)
    entry.delete(0, tk.END)
    message_queue.put(message)

            # Create a thread-safe queue to hold the message


def getmessage(conversation):

    while True:
        if(message_queue==None):
            pass
        else:
            message = message_queue.get()
            conversation.addmessage_human(message)
            return message
            



ct.set_default_color_theme("dark-blue")
app = ct.CTk()
app.title("Ada A.I")
app.geometry("800x600")

chat_area = ct.CTkTextbox(app, height=500, width=700, wrap=tk.WORD, state=tk.DISABLED)
chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")  # Sticky to all sides




entry = ct.CTkEntry(app, width=60)
entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
entry.bind("<Return>", send_message)
entry.configure(state=tk.NORMAL)

send_button = ct.CTkButton(app, text="Send", width=20, command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Configure columns and rows to expand
app.grid_columnconfigure(0, weight=1)  # Chat area column
app.grid_columnconfigure(1, weight=0)  # Button column
app.grid_rowconfigure(0, weight=1)  # Chat area row
app.grid_rowconfigure(1, weight=0)  # Entry and button row





print_color("An Experimental A.I by Daniyal Ahmed", fore_color=Fore.GREEN, back_color=Back.BLACK, style=Style.NORMAL)



#!The Darwin_bot, the first pipeline through which the user input is fed
class Darwin_bot:
 

    
    def __init__(self):
        #!Initializing the Alan bot
        self.alan_bot = Alan()
        self.conversation = Conversation()
        #!JUST FOR EMAILS

        
        #!Consider past response is a boolean that tells the bot if it should consider the past response, this helps it have some sort of short term memory
        #!Further more if the bot needs a true or false response it knows how to bounce back the the function after returing the response
        self.consider_past_response = 1
        #!conservation is appended to let the bot know if it should consider the past responses, and have some sort of short term memory









    def command_line_interface(self, user_input):
        if("./Q&A" in user_input):
            return self.processQnA(user_input.replace("./Q&A",""))
            

        return "unknown"



    #!The main function that processes the user input
    def Darwin_Process(self):
        response = ""

        



        user_input = getmessage(Darwin.conversation)

        response=self.command_line_interface(user_input)

        if(response == "unknown"):
        
            self.conversation.check_derailment()

            user2 = user_input.lower()
    
            result=identify_intent(user2)

            print_color("In Process_Darwin " + response, fore_color=Fore.YELLOW, back_color=Back.BLACK, style=Style.NORMAL)


            #!If the score is greater than .7 then it should consider the response as a true response and not feed it to Alan
            #! The point of this is to give control to some aspects that alan is not capable of doing
            print("functions will go here")
            if(result[0]['label']=="email_requests" and result[0]['score']>.8 ):
                        response= self.email_requests(user_input)
            elif(result[0]['label']=="Save_Response" and result[0]['score']>.5):
                        response= self.save_response(user_input)

            elif(result[0]['label']=="Notion_edit" and result[0]['score']>.6):
                        response= self.notion_edit(user_input)




            else:
                    print("Feeding to Alan")
                    self.consider_past_response= 1
                    response = self.alan_bot.ProcessResponse(user_input)
                    #response = "Alan is not responding right now"
                    append_Darwin(response,self.conversation)
                    self.conversation.addmessage_bot(response)
                    #!if the response meets the geared_responses requirements then it should be fed to the geared_responses model

        else:
            append_Darwin(response,self.conversation)
            self.conversation.addmessage_bot(response)

        


    def notion_edit(self,user_input):
        Date = fetch_labels(user_input, "DATE", undefined="UNKNOWN")
        Keywords = Basic_Keyword_Extractor(user_input)
        if(Date == "UNKNOWN"):
            add_event(Keywords)

        else:
            add_event(Keywords,Date)


        append_Darwin( "Okay I added that to your calender",self.conversation)


    def save_response(self,user_input):
       message = self.conversation.Bots[-1]
       append_Darwin( process_Message(message,self.conversation), self.conversation)
        
       
        
    def email_requests(self,user_input):

        sender = "Daniyal Ahmed"
        

        body = self.alan_bot.ProcessResponse(user_input +"Make sure to start your email with \'Dear Sir/Madam\'")
        

        email = Gmail(user_input, body)

        append_Darwin(email.body,self.conversation)


        append_Darwin("Would you like to send this email ",self.conversation)


        user_input2= getmessage(self.conversation)

        if(Affirm_or_deny(user_input2)=="yes"):
    
                if(email.reciever_email=="UNKNOWN" or email.reciever_name=="Name"):
                    while True:
                        print("stuck here 2nd loop")
                        if(str(email.reciever_email)=="UNKNOWN" and str(email.reciever_name)!="Name"):
                            append_Darwin("Who is the Email For",self.conversation)



                           
                            email.reciever_email = str(fetch_labels(user_input, "EMAIL", undefined="UNKNOWN"))
                        elif(str(email.reciever_email)!="UNKNOWN" and str(email.reciever_name)=="Name"):
                            append_Darwin("Who is the Email For\n",self.conversation)
                            user_input= getmessage(self.conversation)
                            email.reciever_name = fetch_labels(user_input, "PERSON", undefined="Name")
                        elif(str(email.reciever_email)=="UNKNOWN" and str(email.reciever_name)=="Name"):
                            append_Darwin("Who is the Email For, Please write the email as well\n",self.conversation)
                            user_input= getmessage(self.conversation)
                            receiver_email = fetch_labels(user_input, "PERSON", undefined="Name")
                            email.reciever_name = fetch_labels(user_input, "PERSON", undefined="Name")
                            email.reciever_email = fetch_labels(user_input, "EMAIL", undefined="UNKNOWN")
                     
                        elif(str(email.reciever_email)!="UNKNOWN" and str(email.reciever_name)!="Name"):
                             print_color("All paremeters met", fore_color=Fore.GREEN, back_color=Back.BLACK)
                             break
                        
            




                email.body = "Dear "+ str(email.reciever_name) + ",\n\n" + email.body+"\nRegards,\n"+sender
                append_Darwin( email.send_email("No-Subject", email.body, str(email.reciever_email)),self.conversation)


               
    def processQnA(self,user_input):
         list =QuestionAnswering(user_input)

         if(list=="unknown"):
              return "Sorry I couldn't find anything in your notes about that"

         return "According to your notes\""+list[0]+"\", I found this in "+list[1]
         

Darwin = Darwin_bot()


def chatbot_loop():
    while True:
        Darwin.Darwin_Process()
        Darwin.conversation.print()
        print_color("Back in Chatloop " , fore_color=Fore.GREEN, back_color=Back.BLACK, style=Style.NORMAL)




print("Ran")

bot_thread = threading.Thread(target=chatbot_loop)
bot_thread.start()






app.mainloop()
