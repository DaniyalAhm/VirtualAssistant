import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import colorama
from colorama import Fore, Back, Style


def print_color(text, fore_color=Fore.GREEN, back_color=Back.BLACK, style=Style.NORMAL):
    formatted_text = f"{style}{fore_color}{back_color}{text}{Style.RESET_ALL}"
    print(formatted_text)



class Conversation:


    def __init__(self) -> None:
        self.Bots = []
        self.Humans = []


    def addmessage_bot(self, botMessage):
        self.Bots.append(botMessage)

        



    def addmessage_human(self, humanMessage):
        self.Humans.append(humanMessage)

        








    def check_derailment(self):
        messages= self.print()

        if(self.derailed(messages)):
            print_color("Conversation derailed", fore_color=Fore.RED)
    

        else:
            print_color("Conversation has not yet derailed", fore_color=Fore.GREEN)





    def preprocess_text(self, text):
            # Tokenize and remove stopwords from the text
            tokens = word_tokenize(text.lower())
            filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
            return ' '.join(filtered_tokens)




    def derailed(self, current_utterance):
        # If there are no previous utterances, add the current utterance to the list and return False

        self.previous_utterances = self.makecombinedlist()

        if not self.previous_utterances:
            self.previous_utterances.append(current_utterance)
            return False

        # Preprocess the current and previous utterances
        preprocessed_current = self.preprocess_text(current_utterance)
        preprocessed_previous = [self.preprocess_text(utt) for utt in self.previous_utterances]

        # Use TF-IDF vectorization to represent the utterances
        vectorizer = TfidfVectorizer()
        vectorized_previous = vectorizer.fit_transform(preprocessed_previous)
        vectorized_current = vectorizer.transform([preprocessed_current])

        # Calculate cosine similarity between the current and previous utterances
        similarities = cosine_similarity(vectorized_current, vectorized_previous).flatten()

        # If any of the similarities indicate a derailed conversation, return True
        if any(similarity < 0.9 for similarity in similarities):
            self.previous_utterances.append(current_utterance)
            return True
        else:
            self.previous_utterances.append(current_utterance)
            return False


    def print(self):
        result= ""
        for x in range(len(self.Bots)):
            if(x<len(self.Bots)):
                result += self.Bots[x] 
            if(x<len(self.Humans)):
                result +=  self.Humans[x] 

        return result
    
    def makecombinedlist(self):
        result= []
        for x in range(len(self.Bots)):
            if(x<len(self.Bots)):
                result.append( self.Bots[x]) 
            if(x<len(self.Humans)):
               result.append(  self.Humans[x]) 
            

        return result
    