from docx import Document
import pdfplumber
import os
import pdfplumber
import json
import sys

sys.path.append("/home/daniyal-ahmed/Documents/VirtualAssistant/A.I learning V.58/Darwin")
from Basic_nlp_functions import generate_title
from ConversationDataStruct import *

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def saveAsPdf(text, filename):

    pdf_filename = os.path.join("/home/daniyal-ahmed/Downloads", filename+".pdf")

    c = canvas.Canvas(pdf_filename, pagesize=letter)
    
    # Split the text into lines
    lines = text.split('\n')
    
    # Set the starting position for drawing text
    x, y = 50, 750
    
    # Loop through the lines and draw them on the PDF
    for line in lines:
        c.drawString(x, y, line)
        y -= 15  # Move up for the next line
    
    # Save the PDF file
    c.save()






def findformat(conversation):
    for message in conversation.Humans:
        if 'multiple choice' in message.lower():
            return "multiple choice"
        
    for message in conversation.Bots:
        if 'multiple choice' in message.lower():
            return "multiple choice"

    return 'code'




def process_Message(message,conversation):
    with open('/home/daniyal-ahmed/Documents/VirtualAssistant/A.I learning V.58/Darwin/Functionalities/code_words.json', 'r') as file:
    # Load the JSON content into a Python object
         data = json.load(file)


    extensions = {
        "JavaScript": ".js",
        "Python": ".py", 
        "Java": ".java",
        "C#": ".cs",
        "PHP": ".php",
        "C++": ".cpp", 
        "C": ".c",
        "R": ".r",
        "Objective-C": ".m",
        "Swift": ".swift",
        "TypeScript": ".ts",
        "Ruby": ".rb",
        "Go": ".go",
        "Assembly": ".asm",
        "PowerShell": ".ps1",
        "Haskell": ".hs",
        "Perl": ".pl",
        "Kotlin": ".kt",
        "Scala": ".scala",
        "Shell": ".sh",
        "Rust": ".rs", 
        "Lua": ".lua"
        }

    format1 = findformat(conversation)  
    print(format1)

    if format1 == "multiple choice":
        if "1." in message:
            message = message["1.":]
    elif format1 == 'code':
        print("in elif condition")
        key=find_language(message,conversation)
        codewords = data[key]    
        extension= extensions[key]
        for x in message:
            if x in codewords:
                message = message[x:]

        title = generate_title(conversation.print(),5)
        filename = os.path.join("/home/daniyal-ahmed/Downloads", title+extension)

        with open(filename, "w") as f:

            f.write(message)

        return "I have saved the file as "+filename+" in your Downloads folder"


                

    title = generate_title(conversation.print(), 5)

    title.replace(" ","_")

    saveAsPdf(message,title)

    return "I have saved the file as "+title+".pdf in your Downloads Folder"


def find_language(prompt, conversation):
    with open('/home/daniyal-ahmed/Documents/VirtualAssistant/A.I learning V.58/Darwin/Functionalities/code_words.json', 'r') as file:
    # Load the JSON content into a Python object
         data = json.load(file)



    context = conversation.print()


    for key in data:
        if key.lower() in context.lower():
            return key



    max_count=0
    count = 0
    langauage = ""
    for key in data:
        current_list = data[key]
        for word in current_list:
            if word in prompt:
                count+=1
        if count > max_count:
            max_count = count
            language = key

    return language
