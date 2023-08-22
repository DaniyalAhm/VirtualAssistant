from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
import json
#from sklearn.model_selection import train_test_split

from transformers import TextClassificationPipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
import colorama
from colorama import Fore, Back, Style

def print_color(text, fore_color=Fore.GREEN, back_color=Back.BLACK, style=Style.NORMAL):
    formatted_text = f"{style}{fore_color}{back_color}{text}{Style.RESET_ALL}"
    print(formatted_text)



def identify_intent(user_input):
    # Replace with the path to your fine-tuned model checkpoint directory and checkpoint name
    model_checkpoint_path = "/home/daniyal-ahmed/Documents/VirtualAssistant/A.I learning V.58/Fine_Tuned_BERT18/checkpoint-75"


    # Load the tokenizer and model with the specific checkpoint
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint_path)

    # Create the text classification pipeline
    intent_recog = TextClassificationPipeline(model=model, tokenizer=tokenizer)
    print("Identifying intent...")
    # Perform inference on a sample text
    result = intent_recog(user_input)
    print(result)
    return result


identify_intent(" put concert on my calender")

random_requests_questions = [
     "Could you please save this file?",
    "Would you mind saving this file?",
    "Can you save this document?",
    "Is it possible for you to save this file?",
    "Are you able to save this document?",
    "I need you to save this file, could you?",
    "Please save this file for me.",
    "Could you perform a save on this file?",
    "Would you be kind enough to save this file?",
    "If you can, please save this document?",
    "Can you save and update this file?",
    "Kindly save this file at your earliest convenience.",
    "May I request you to save this document?",
    "Please don't forget to save this file.",
    "It would be great if you could save this file.",
    "Can you perform a save operation on this file?",
    "Please ensure you save this document.",
    "If you're able, please save this file.",
    "I'd appreciate it if you could save this file.",
    "Would you be willing to save this document?",
    "Could you save this file when you have a moment?",
    "Is there a chance you could save this file?",
    "If possible, could you save this document?",
    "Can you save and store this file, please?",
    "It'd be fantastic if you could save this file.",
    "Would you kindly save this document for me?",
    "If it's not too much trouble, save this file.",
    "Can you save this file and update the changes?",
    "Could you possibly save this document?",
    "Would you be able to save this file?",
    "Can you make sure to save this file?",
    "Please add a save action to this file.",
    "Is saving this file within your capabilities?",
    "Could you execute a save for this document?",
    "Would you be open to saving this file?",
    "Please don't omit to save this file.",
    "Is saving this file something you can do?",
    "Can you save this file right now?",
    "Could you perform a save on this document?",
    "Would you consider saving this file?",
    "Can you save this file promptly?",
    "Are you capable of saving this document?",
    "Could you possibly save this file for me?",
    "Would you be so kind as to save this file?",
    "Can you do a quick save of this document?",
    "Could you save this file without delay?",
    "Would you be up for saving this file?",
    "Can you save this file and keep it secure?",
    "Could you save this document without hesitation?",
    "Would you mind saving this file when possible?",
    "Can you save this file and retain the changes?",
    "Could you possibly save this document?",
    "Would you be able to save this file promptly?",
    "Can you ensure to save this file for me?",
    "Could you save this file and update the modifications?",
    "Would you be kind enough to save this file?",
    "Can you perform a save operation on this document?",
    "Could you save this file in a timely manner?",
    "Would you be willing to save this file for me?",
    "Can you save this file and safeguard the data?",
    "Could you possibly save and store this document?",
    "Would you kindly save this file when convenient?",
    "Can you save this file with urgency?",
    "Could you execute a save on this file?",
    "Would you consider saving this document for me?",
    "Can you save this file and make sure changes are applied?",
    "Could you save this file and prevent data loss?",
    "Would you be open to saving this document for me?",
    "Can you save this file immediately?",
    "Could you perform a save action on this file?",
    "Would you consider saving this file at your earliest opportunity?",
    "Can you save this file with quick action?",
    "Could you save this file expeditiously and with accuracy?",
    "Would you be open to saving this file without any delay?",
    "Can you save this file without any additional waiting?",
    "Could you perform a save on this file without any further ado?",
    "Would you mind saving this document promptly?",
    "Can you save this file urgently while maintaining integrity?",
    "Could you possibly save this document with immediate effect?",
    "Would you be able to save this file right away and without any procrastination?",
    "Can you save this file and ensure that changes take effect?",
    "Could you save this file and preserve its original state?",
    "Would you be willing to save this document without any unnecessary pause?",
    "Can you save this file swiftly and immediately?",
    "Could you execute a save operation on this file without hesitation?",
    "Would you consider saving this file at your earliest opportunity?",
    "Can you save this file with quick action?",
    "Could you save this file expeditiously and with accuracy?",
    "Would you be open to saving this file without any delay?",
    "Can you save this file without any additional waiting?",
    "Could you perform a save on this file without any further ado?",
    "Would you mind saving this document promptly?",
    "Can you save this file urgently while maintaining integrity?",
    "Could you possibly save this document with immediate effect?",
    "Would you be able to save this file right away and without any procrastination?"
]

def checker( ):
    with open('/home/daniyal-ahmed/Documents/VirtualAssistant/A.I learning V.58/Datasets/Geared_Responsed4.json', 'r') as file:
        # Load the JSON content into a Python object
            data = json.load(file)



    count=0
    total = 0
    email_res= []
    save_res = []
    notion_res =[]
    for key in data:
        print("The Key is ", key)
        for sentence in data[key]:
            print(sentence)
            total+=1
            result = identify_intent(sentence)
            if(result[0]['label']=="email_requests" and result[0]['score']>.8 and key == result[0]['label']):
                            print_color("Pass")
                            count+=1
                            email_res.append(sentence)
            elif(result[0]['label']=="Save_Response" and result[0]['score']>.5 and key == result[0]['label']):
                            print_color("PASS!")
                            count+=1
                            save_res.append(sentence)


            elif(result[0]['label']=="Notion_edit" and result[0]['score']>.5 and key == result[0]['label'] ):
                            print_color("PASS")
                            count+=1
                            notion_res.append(sentence)

            elif(key=="who_are_you" and result[0]['score']>.3 and "False_Positives" == result[0]['label'] ):
                            print_color("PASS")
                            count+=1
                        

            
            else: 
                print_color("FAIL", Fore.RED)
            
    print(f"Pass Rate:{count/total}")
    print(f"The Ones that got confused for emails {email_res}")
    print(f"The Ones that got confused for Notion {notion_res}")
    print(f"The Ones that got confused for Saves {save_res}")


