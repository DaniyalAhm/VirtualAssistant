import spacy
from spacy import displacy
import requests

import spacy
from dateutil.parser import parse
from parsedatetime import Calendar
from transformers import BertModel
import torch
from fuzzywuzzy import fuzz
from transformers import pipeline,AutoTokenizer, AutoModelForSeq2SeqLM



API_URL = "https://api-inference.huggingface.co/models/dslim/bert-base-NER"
headers = {"Authorization": "Bearer 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"}



#!Use this to help you use more models from the internet
def generate_title(input_text, max_title_length=10):
    # Load model directly

    tokenizer = AutoTokenizer.from_pretrained("czearing/article-title-generator")
    model = AutoModelForSeq2SeqLM.from_pretrained("czearing/article-title-generator")


    inputs = tokenizer(input_text, return_attention_mask=False, return_token_type_ids=False, return_tensors="pt")


    # Generate a title
    with torch.no_grad():
        output = model.generate(inputs.input_ids, max_length=max_title_length, num_return_sequences=1)
    
    generated_title = tokenizer.decode(output[0], skip_special_tokens=True)
    final_title = generated_title.capitalize()
    
    return final_title














def Affirm_or_deny(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text.lower())  # Convert text to lowercase for case-insensitive matching
    
    affirmations = ["yes", "yeah", "yep", "sure", "absolutely", "certainly", "definitely"]
    denials = ["no", "nope", "nah", "not really", "negative", "never"]
    
    for token in doc:
        token_text = token.text
        
        for affirmation in affirmations:
            similarity = fuzz.ratio(token_text, affirmation)
            if similarity >= 80:  # You can adjust this threshold as needed
                return "yes"
        
        for denial in denials:
            similarity = fuzz.ratio(token_text, denial)
            if similarity >= 80:  # You can adjust this threshold as needed
                return "no"
    
    return "Unknown"


def name_file(prompt):
    nouns = fetch_nouns(prompt)
    item_counts = {}

    for item in nouns:
        item_counts[item] = item_counts.get(item, 0) + 1

    # Find the item with the highest count
    most_frequent_item = max(item_counts, key=item_counts.get)

    return most_frequent_item 


def fetch_labels(text, entity_label, undefined="undefined"):
    nlp = spacy.load("en_core_web_lg")
    text_doc = nlp(text)




    if entity_label.upper() == "PERSON":
        for word in text_doc.ents:
            if word.label_ == "PERSON":
                return word.text

    elif entity_label.upper() == "EMAIL":
        for ent in text_doc:
            if ent.like_email:
                return ent
            



    elif entity_label.upper() == "DATE":
        months_lower = [
         "january", "february", "march", "april",
        "may", "june", "july", "august", "september",
        "october", "november", "december"]   
        months_upper = [
    "January", "February", "March", "April",
    "May", "June", "July", "August", "September",
    "October", "November", "December"]
              

              
        for x in range (len(months_lower)):
            if months_lower[x] in text:
                text = text.replace(months_lower[x], months_upper[x])

        text_doc = nlp(text)


        dates = []
        cal = Calendar()
        for token in text_doc:
            if token.ent_type_ == "DATE" or token.like_num:
                dates.append(token.text)

        

        dat_str=""
        for item in dates:
            dat_str = dat_str + " " + item

        if(len(dat_str) == 0):
            return undefined

        parsed_date = parse(dat_str, fuzzy=True)

        return parsed_date.isoformat()
    return undefined




def email_body_extractor(text):
    nlp = spacy.load("en_core_web_sm")


    doc = nlp(text)

    sentences = list(doc.sents)
    paragraphs =""
    for sentence in sentences:
        paragraphs = paragraphs + " " + sentence.text


    return paragraphs




def fetch_nouns(prompt):
    prompt = prompt.lower()
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(prompt)
    nouns = []
    for token in doc:
        if token.pos_ == "NOUN":
            nouns.append(token.text)
    return nouns



def Basic_Keyword_Extractor(prompt):
    nouns = fetch_nouns(prompt)
    dataset = ["calender", "schedule", "event", "appointment", "meeting", "reminder", "notion"]
    title=""
    for item in nouns: 
        if item not in dataset:
           title = title + " " + item
        

    return title 
    


def Advanced_Keyword_Extractor(prompt):
    device = torch.device("cpu") # or "cuda" if you are using GPU
    model = BertModel.load_weight("./bert", device=device)
    inputs = {
            'inputs': torch.tensor([[sentence.lowered]]),
        }
        
    outputs = model.predict(**inputs)[0]
        
    tokenizer = torch.utils.num2str(outputs).split()
        
    return tokenizer[-1:]




def summerize_text(text):
    from transformers import BartTokenizer, BartForConditionalGeneration, pipeline

 
    # Load the model and tokenizer
    model_name = "com3dian/Bart-large-paper2slides-summarizer"
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)

    # Generate summary from input text
    input_ids = tokenizer.encode(text, return_tensors="pt")
    output = model.generate(input_ids)

    # Decode generated summaries
    summary = tokenizer.decode(output[0], skip_special_tokens=True)
    print(summary)





#!NOT IN USE
'''
def fetch_labels(text, entity_label, undefined= "undefined"):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    for token in doc:
        if token.pos_ == entity_label:
            return token.text

    return undefined

# Example usage:
text = "Apple Inc. is a technology company headquartered in California."
entity_label_to_find = "ORG"



# Define a function to find and annotate people's names as entities
def find_people_entities(text):
    doc = nlp(text)
    person_spans = []

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            person_spans.append(doc.char_span(ent.start_char, ent.end_char, label="PERSON"))

    # Add the new entity spans to the document's entities
    doc.ents = list(doc.ents) + person_spans

    return doc




def Namefinder(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	response= response.json()[0]['word']

output = Namefinder({
	"inputs": "My name is Daniyal",
})
'''


