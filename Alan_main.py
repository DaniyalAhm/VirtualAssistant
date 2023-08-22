import sys
#from PyQt5.QtWinExtras import QtWin
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QWidget
from hugchat import hugchat
import json


#TODO Add the clear conversations when the window is exited a
#TODO Add PDF capabilities
#TODO Add image Detection Capabilties
#TODO ADD IMAGE TO TEXT CAPABILITIES
#TODO Add TEXT to Image Capabilties
#TODO Make Ui more Appealing
#!Make Document Creation capabilities


class Alan():
 
        

    def __init__(self):
        self.chat=  "test"
        self.chatbot = hugchat.ChatBot(cookie_path="/home/daniyal-ahmed/Documents/VirtualAssistant/A.I learning V.58/Darwin/Alan_/cookies.json")
        self.id = self.chatbot.new_conversation()
        self.chatbot.change_conversation(self.id)
        self.current_internet_status = True



    def ProcessResponse(self,user_input):
    
        return  self.chatbot.chat(user_input)
    

    def Switch_internet(self):

        if(self.current_internet_status == True):
            self.chatbot= hugchat.ChatBot(cookie_path="F:\\A.I learning V.4\\Darwin\Alan_\\cookies.json")
            self.current_internet_status = False
            return "Internet has been turned off"
        
        self.current_internet_status = True
        self.chatbot= hugchat.ChatBot(cookie_path="Alan\cookies.json")
        return "Internet has been turned on"



        




