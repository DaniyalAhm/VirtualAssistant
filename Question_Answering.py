from transformers import pipeline
import os
import pdfplumber
import json

# Replace this with your own checkpoint
model_checkpoint = "huggingface-course/bert-finetuned-squad"
question_answerer = pipeline("question-answering", model=model_checkpoint)

directories = ["/home/daniyal-ahmed/Documents/Work2","/home/daniyal-ahmed/Documents/TestforVA"]


def load_in_data(directory):
    contents = {}

    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                md_text = file.read()
                md_text.replace("\n","")
                contents[filename] = md_text
                
                print(filename)
        elif filename.endswith('.pdf'):
            pdf_path = os.path.join(directory, filename)
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text()

                    text.replace("\n","")
                    text.replace("\"",'')
            contents[filename] = text
            print(filename)

    return contents

def updateQandA(Directories):
    FinalDict = {}
    
    for Directory in Directories:
        FinalDict.update(load_in_data(Directory))

    json_file_path = 'contents.json'
    with open(json_file_path, 'w') as json_file:
        json.dump(FinalDict, json_file, indent=4)


updateQandA(directories)


def QuestionAnswering(question):
    with open("/home/daniyal-ahmed/Documents/VirtualAssistant/contents.json", "r") as json_file:
        json_data = json_file.read()

    Context = json.loads(json_data)

    max_score = 0
    answer = ""
    keyMain=""
    for key, value in Context.items():
        result = question_answerer(question, value)
        if result['score'] > max_score:
            max_score = result['score']
            answer = result['answer']
            keyMain = key

   



    return [answer, keyMain]

def pdf_to_text_and_save(pdf_path, text_output_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        
        # Save the extracted text to a text file
        with open(text_output_path, "w", encoding="utf-8") as text_file:
            text_file.write(text)





